require("@nomicfoundation/hardhat-toolbox");
const { task } = require("hardhat/config");
require("dotenv").config();

// https://hardhat.org/guides/create-task.html
task("accounts", "Prints the list of accounts", async (taskArgs, hre) => {
  const accounts = await hre.ethers.getSigners();

  for (const account of accounts) {
    console.log(account.address);
  }
});

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.20",
  networks: {
    default: {
      url: process.env.CHAIN_URL || "",
      accounts:
        process.env.PRIVATE_KEY !== undefined
          ? process.env.PRIVATE_KEY.split(",")
          : [],
      chainId: process.env.CHAIN_ID,
    },
  },
};
