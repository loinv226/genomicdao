// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

interface IGeneNFT {
    event MintGeneNFT(address indexed owner, uint256 id);

    function safeMint(address to) external returns (uint256);
}
