// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./interfaces/IPCSPToken.sol";

contract PCSPToken is ERC20, IPCSPToken, ERC20Burnable, Ownable {
    mapping(uint256 => uint256) riskScoreToAward;

    constructor()
        ERC20("Post-Covid Stroke Prevention", "PCSP")
        Ownable(_msgSender())
    {
        _mint(msg.sender, 1000000000 * 10 ** decimals());

        riskScoreToAward[1] = 15000 * 10 ** decimals();
        riskScoreToAward[2] = 3000 * 10 ** decimals();
        riskScoreToAward[3] = 225 * 10 ** decimals();
        riskScoreToAward[4] = 30 * 10 ** decimals();
    }

    function mintPCSP(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }

    function reward(
        address to,
        uint256 riskScore,
        string memory geneId
    ) external onlyOwner returns (uint256) {
        // TODO: Implement this method: Award PCSP to the user based on his/her risk score
        // Check to address
        require(to != address(0), "Token: to address must be not empty");
        // Check risk score range
        require(
            riskScore > 0 && riskScore < 5,
            "Token: No reward for the risk score"
        );
        // convert risk score to token
        uint256 mintAmount = riskScoreToAward[riskScore];
        require(mintAmount > 0, "PCSPToken: Mint amount must greater than 0");
        // Mint new PCSP tokens to user
        _mint(to, mintAmount);
        emit MintPCSP(to, mintAmount, geneId);

        return mintAmount;
    }
}
