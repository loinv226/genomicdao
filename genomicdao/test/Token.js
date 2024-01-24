const {
  time,
  loadFixture,
  reset,
} = require("@nomicfoundation/hardhat-toolbox/network-helpers");
const { expect } = require("chai");

describe("Token", function () {
  before(async function () {
    await reset();
  });

  async function deployTokenFixture() {
    const [owner, addr1, addr2] = await ethers.getSigners();

    const pcspToken = await ethers.deployContract("PCSPToken");

    return { pcspToken, owner, addr1, addr2 };
  }

  describe("Deployment", function () {
    it("Should set the right name", async function () {
      const { pcspToken } = await loadFixture(deployTokenFixture);

      expect(await pcspToken.name()).to.equal("Post-Covid Stroke Prevention");
      expect(await pcspToken.symbol()).to.equal("PCSP");
    });

    it("Should set the right total supply", async function () {
      const { pcspToken, owner } = await loadFixture(deployTokenFixture);

      const ownerBalance = await pcspToken.balanceOf(owner.address);

      expect(await pcspToken.totalSupply()).to.equal(
        BigInt("1000000000000000000000000000")
      );
      expect(await pcspToken.totalSupply()).to.equal(ownerBalance);
    });
  });

  describe("Mint", function () {
    it("Should mint the right amount", async function () {
      const { pcspToken, addr1 } = await loadFixture(deployTokenFixture);

      await pcspToken.mintPCSP(addr1, BigInt("1000"));

      const newSupply = BigInt("1000000000000000000000000000") + BigInt("1000");

      expect(await pcspToken.totalSupply()).to.equal(newSupply);
    });

    it("Should mint to correct owner", async function () {
      const { pcspToken, addr1 } = await loadFixture(deployTokenFixture);

      await pcspToken.mintPCSP(addr1, BigInt("1000"));

      const ownerBalance = await pcspToken.balanceOf(addr1.address);

      expect(ownerBalance).to.equal(BigInt("1000"));
    });
  });

  describe("Award token", function () {
    it("Should award the right amount of extremely high risk", async function () {
      const { pcspToken, addr1 } = await loadFixture(deployTokenFixture);

      const awardAmount = BigInt("15000") * BigInt("10") ** BigInt("18");

      const docId = "doc1";
      await pcspToken.reward(addr1, 1, docId);

      const ownerBalance = await pcspToken.balanceOf(addr1.address);

      expect(ownerBalance).to.equal(awardAmount);
    });

    it("Should award the right amount of high risk", async function () {
      const { pcspToken, addr1 } = await loadFixture(deployTokenFixture);

      const awardAmount = BigInt("3000") * BigInt("10") ** BigInt("18");

      const docId = "doc1";
      await pcspToken.reward(addr1, 2, docId);

      const ownerBalance = await pcspToken.balanceOf(addr1.address);

      expect(ownerBalance).to.equal(awardAmount);
    });

    it("Should award the right amount of slightly high risk", async function () {
      const { pcspToken, addr1 } = await loadFixture(deployTokenFixture);

      const awardAmount = BigInt("225") * BigInt("10") ** BigInt("18");

      const docId = "doc1";
      await pcspToken.reward(addr1, 3, docId);

      const ownerBalance = await pcspToken.balanceOf(addr1.address);

      expect(ownerBalance).to.equal(awardAmount);
    });

    it("Should award the right amount of normal or low risk", async function () {
      const { pcspToken, addr1 } = await loadFixture(deployTokenFixture);

      const awardAmount = BigInt("30") * BigInt("10") ** BigInt("18");

      const docId = "doc1";
      await pcspToken.reward(addr1, 4, docId);

      const ownerBalance = await pcspToken.balanceOf(addr1.address);

      expect(ownerBalance).to.equal(awardAmount);
    });

    it("Should revert with invalid risk score", async function () {
      const { pcspToken, addr1 } = await loadFixture(deployTokenFixture);

      await expect(pcspToken.reward(addr1, 5, "doc1")).to.be.revertedWith(
        "Token: No reward for the risk score"
      );
    });
  });
});
