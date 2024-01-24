const fs = require("fs");

const GENE_NFT = "GeneNFT";
const PCSP_TOKEN = "PCSPToken";
const CONTROLLER_CONTRACT = "Controller";

async function getEnvInfo(ethers) {
  // Not need check env, if not exist then can't run script
  const [deployer] = await ethers.getSigners();
  const envInfo = {
    deployer: deployer.address,
    chainId: process.env.CHAIN_ID,
    rpc: process.env.CHAIN_URL,
  };
  return envInfo;
}

// deploy and return contract info
async function deployGeneNFTContract() {
  const GeneNFT = await ethers.getContractFactory(GENE_NFT);
  const _contract = await GeneNFT.deploy();
  await _contract.waitForDeployment();

  return {
    contractName: GENE_NFT,
    address: _contract.target,
  };
}

// deploy and return contract info
async function deployPCSPTokenContract() {
  const PCSPToken = await ethers.getContractFactory(PCSP_TOKEN);
  const _contract = await PCSPToken.deploy();
  await _contract.waitForDeployment();

  return {
    contractName: PCSP_TOKEN,
    address: _contract.target,
  };
}

// deploy and return contract info
async function deployControllerContract(nftAddress, pcspTokenAddress) {
  const ControllerContract = await ethers.getContractFactory(
    CONTROLLER_CONTRACT
  );
  const _contract = await ControllerContract.deploy(
    nftAddress,
    pcspTokenAddress
  );
  await _contract.waitForDeployment();

  return {
    contractName: CONTROLLER_CONTRACT,
    address: _contract.target,
  };
}

// Write contract address into controller contract
async function transferOwnership(
  ctlContractAddress,
  geneNFTAddress,
  pcspTokenAddress
) {
  const GeneNFT = await ethers.getContractFactory(GENE_NFT);
  const PCSPToken = await ethers.getContractFactory(PCSP_TOKEN);
  _geneNFT = await GeneNFT.attach(geneNFTAddress);
  _pcspToken = await PCSPToken.attach(pcspTokenAddress);

  const tx1 = await _geneNFT.transferOwnership(ctlContractAddress);
  const tx2 = await _pcspToken.transferOwnership(ctlContractAddress);
  await tx1.wait();
  await tx2.wait();
}

async function writeToFile(file, data) {
  let _data = JSON.stringify(data);
  fs.writeFileSync(file, _data);
  console.log("-> Artifacts path: ", file);
}

module.exports = {
  getEnvInfo,
  deployControllerContract,
  deployGeneNFTContract,
  deployPCSPTokenContract,
  transferOwnership,
  writeToFile,
};
