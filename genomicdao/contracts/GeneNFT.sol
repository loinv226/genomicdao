// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./interfaces/IGeneNFT.sol";

// Counters.sol removed from openzeppelin
// import "@openzeppelin/contracts/utils/Counters.sol";

contract GeneNFT is ERC721, IGeneNFT, ERC721Burnable, Ownable {
    // Address of controller contract
    uint256 private _idCounter;

    constructor() ERC721("GeneNFT", "GNFT") Ownable(_msgSender()) {}

    function safeMint(address to) external onlyOwner returns (uint256) {
        _safeMint(to, ++_idCounter);
        emit MintGeneNFT(to, _idCounter);

        return _idCounter;
    }
}
