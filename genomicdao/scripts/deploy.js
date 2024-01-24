// We require the Hardhat Runtime Environment explicitly here. This is optional
// but useful for running the script in a standalone fashion through `node <script>`.
//
// You can also run a script with `npx hardhat run <script>`. If you do that, Hardhat
// will compile your contracts, add the Hardhat Runtime Environment's members to the
// global scope, and execute the script.

const { ethers, getChainId } = require("hardhat");
const task = require("./task");

async function main() {
  const envInfo = await task.getEnvInfo(ethers);

  const geneNFTInfo = await task.deployGeneNFTContract();
  const pcspTokenInfo = await task.deployPCSPTokenContract();
  const ctlContractInfo = await task.deployControllerContract(
    geneNFTInfo.address,
    pcspTokenInfo.address
  );
  // await task.transferOwnership(
  //   ctlContractInfo.address,
  //   geneNFTInfo.address,
  //   pcspTokenInfo.address
  // );

  envInfo.ctlContractInfo = ctlContractInfo;
  envInfo.geneNFTInfo = geneNFTInfo;
  envInfo.pcspTokenInfo = pcspTokenInfo;

  console.log("-> Deploy info: \n", envInfo);
  task.writeToFile(`artifacts-${new Date().toISOString()}.json`, envInfo);
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
