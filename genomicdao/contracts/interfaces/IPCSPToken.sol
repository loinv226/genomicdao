// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

interface IPCSPToken {
    event MintPCSP(address indexed to, uint256 amounnt, string geneId);

    function mintPCSP(address to, uint256 amount) external;

    function reward(
        address to,
        uint256 riskScore,
        string memory geneId
    ) external returns (uint256);
}
