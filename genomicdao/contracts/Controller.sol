// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// Counters.sol removed from openzeppelin
// import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

import "./interfaces/IGeneNFT.sol";
import "./interfaces/IPCSPToken.sol";

contract Controller is Ownable {
    //
    // STATE VARIABLES
    //
    uint256 private _sessionIdCounter;
    IGeneNFT public geneNFT;
    IPCSPToken public pcspToken;

    struct UploadSession {
        uint256 id;
        address user;
        string proof;
        bool confirmed;
    }

    struct DataDoc {
        string id;
        string hashContent;
    }

    // To check session exist
    mapping(uint256 => UploadSession) sessions;
    // Doc submited
    mapping(string => DataDoc) docs;
    // Check doc submited
    mapping(string => bool) docSubmits;
    mapping(uint256 => string) nftDocs;

    //
    // EVENTS
    //
    event UploadData(address user, string docId, uint256 sessionId);
    event UploadSuccess(
        address user,
        string docId,
        uint256 sessionId,
        uint256 nftId,
        uint256 tokenAmount,
        string proof
    );

    // Modifiers
    modifier notExistDocSubmited(string memory docId) {
        require(!docSubmits[docId], "Controller: doc submited");
        _;
    }

    modifier mustContainSession(uint256 sessionId, address user) {
        require(
            sessions[sessionId].id > 0 && sessions[sessionId].user == user,
            "Controller: session not valid"
        );
        _;
    }

    constructor(address nftAddress, address pcspAddress) Ownable(_msgSender()) {
        geneNFT = IGeneNFT(nftAddress);
        pcspToken = IPCSPToken(pcspAddress);
    }

    function uploadDoc(
        address user,
        string memory docId,
        string memory proof,
        bool confirmed
    ) external onlyOwner notExistDocSubmited(docId) {
        // TODO: Implement this method: to start an uploading gene data session. The doc id is used to identify a unique gene profile. Also should check if the doc id has been submited to the system before. This method return the session id

        // Get new session id
        _sessionIdCounter++;
        uint256 sessionId = _sessionIdCounter;

        // Save and return session
        sessions[sessionId] = UploadSession(sessionId, user, proof, confirmed);

        // Emit event
        emit UploadData(user, docId, sessionId);
    }

    function confirm(
        address user,
        string memory docId,
        string memory hashContent,
        string memory proof,
        uint256 sessionId,
        uint256 riskScore
    )
        external
        onlyOwner
        notExistDocSubmited(docId)
        mustContainSession(sessionId, user)
    {
        // TODO: Implement this method: The proof here is used to verify that the result is returned from a valid computation on the gene data. For simplicity, we will skip the proof verification in this implementation. The gene data's owner will receive a NFT as a ownership certicate for his/her gene profile.
        // TODO: Verify proof, we can skip this step
        // Update doc content
        docs[docId] = DataDoc(docId, hashContent);
        docSubmits[docId] = true;
        // Mint NFT
        uint256 nftId = geneNFT.safeMint(user);

        // Reward PCSP token based on risk stroke
        uint256 tokenAmount = pcspToken.reward(user, riskScore, docId);

        // Emit event
        emit UploadSuccess(user, docId, sessionId, nftId, tokenAmount, proof);

        // Close session
        delete sessions[sessionId];
    }

    function getSession(
        uint256 sessionId
    ) public view returns (UploadSession memory) {
        return sessions[sessionId];
    }

    function getDoc(string memory docId) public view returns (DataDoc memory) {
        return docs[docId];
    }
}
