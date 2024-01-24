const {
  time,
  loadFixture,
  reset,
} = require("@nomicfoundation/hardhat-toolbox/network-helpers");

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Controller", function () {
  before(async function () {
    await reset();
  });

  async function deployControllerFixture() {
    const [owner, addr1, addr2] = await ethers.getSigners();

    const nft = await ethers.deployContract("GeneNFT");
    const pcspToken = await ethers.deployContract("PCSPToken");
    const controller = await ethers.deployContract("Controller", [
      nft.target,
      pcspToken.target,
    ]);

    await nft.transferOwnership(controller.target);
    await pcspToken.transferOwnership(controller.target);

    return { controller, nft, pcspToken, owner, addr1, addr2 };
  }

  describe("Upload Data", function () {
    it("Should receive session id", async function () {
      const { controller, addr1, addr2 } = await loadFixture(
        deployControllerFixture
      );

      const proof = "success";
      const docId = "doc1";
      await expect(controller.uploadData(addr2, docId, proof, true)).to.emit(
        controller,
        "UploadData"
      );
      // .withArgs(addr2, docId, 1);
    });

    it("Should fail if the doc is submited", async function () {
      const { controller, addr1, addr2 } = await loadFixture(
        deployControllerFixture
      );

      const docId = "doc1";
      const contentHash = "dochash";
      const proof = "success";
      const riskScore = 1;
      const sessionId = 1;

      await controller.uploadData(addr1, docId, proof, true);
      await controller.confirm(
        addr1,
        docId,
        contentHash,
        proof,
        sessionId,
        riskScore
      );

      await expect(
        controller.uploadData(addr1, docId, proof, true)
      ).to.be.revertedWith("Controller: doc submited");
    });
  });

  describe("Confirm data", function () {
    it("Should receive correct nft", async function () {
      const { controller, nft, owner, addr1 } = await loadFixture(
        deployControllerFixture
      );

      const docId = "doc1";
      const contentHash = "dochash";
      const proof = "success";
      const riskScore = 1;
      const sessionId = 1;

      await controller.uploadData(addr1, docId, proof, true);
      await controller.confirm(
        addr1,
        docId,
        contentHash,
        proof,
        sessionId,
        riskScore
      );

      expect(await nft.ownerOf(1)).to.equal(addr1.address);
    });

    it("Should receive correct pcsp reward", async function () {
      const { controller, pcspToken, addr1 } = await loadFixture(
        deployControllerFixture
      );

      const docId = "doc1";
      const contentHash = "dochash";
      const proof = "success";
      const riskScore = 1;
      const sessionId = 1;

      const awardAmount = BigInt("15000") * BigInt("10") ** BigInt("18");

      await controller.uploadData(addr1, docId, proof, true);
      await controller.confirm(
        addr1,
        docId,
        contentHash,
        proof,
        sessionId,
        riskScore
      );

      const ownerBalance = await pcspToken.balanceOf(addr1.address);

      expect(ownerBalance).to.equal(awardAmount);
    });

    it("Should close session", async function () {
      const { controller, addr1 } = await loadFixture(deployControllerFixture);

      const docId = "doc1";
      const contentHash = "dochash";
      const proof = "success";
      const riskScore = 1;
      const sessionId = 1;

      await controller.uploadData(addr1, docId, proof, true);
      await controller.confirm(
        addr1,
        docId,
        contentHash,
        proof,
        sessionId,
        riskScore
      );

      const session = await controller.getSession(sessionId);

      expect(session.proof).to.equal("");
      expect(session.confirmed).to.equal(false);
    });

    it("Should content hash uploaded", async function () {
      const { controller, addr1 } = await loadFixture(deployControllerFixture);

      const docId = "doc1";
      const contentHash = "dochash";
      const proof = "success";
      const riskScore = 1;
      const sessionId = 1;

      await controller.uploadData(addr1, docId, proof, true);
      await controller.confirm(
        addr1,
        docId,
        contentHash,
        proof,
        sessionId,
        riskScore
      );

      const doc = await controller.getDoc(docId);

      expect(doc.hashContent).to.equal(contentHash);
    });

    it("Should fail if the doc is submitted", async function () {
      const { controller, addr1 } = await loadFixture(deployControllerFixture);

      const docId = "doc1";
      const contentHash = "dochash";
      const proof = "success";
      const riskScore = 1;
      const sessionId = 1;

      await controller.uploadData(addr1, docId, proof, true);
      await controller.confirm(
        addr1,
        docId,
        contentHash,
        proof,
        sessionId,
        riskScore
      );

      await expect(
        controller.confirm(
          addr1,
          docId,
          contentHash,
          proof,
          sessionId,
          riskScore
        )
      ).to.be.revertedWith("Controller: doc submited");
    });

    it("Should fail if the session owner is invalid", async function () {
      const { controller, addr1, addr2 } = await loadFixture(
        deployControllerFixture
      );

      const docId = "doc1";
      const contentHash = "dochash";
      const proof = "success";
      const riskScore = 1;
      const sessionId = 1;

      await controller.uploadData(addr1, docId, proof, true);

      await expect(
        controller.confirm(
          addr2,
          docId,
          contentHash,
          proof,
          sessionId,
          riskScore
        )
      ).to.be.revertedWith("Controller: session not valid");
    });

    it("Should fail if the session is end", async function () {
      const { controller, addr1 } = await loadFixture(deployControllerFixture);

      const docId = "doc1";
      const docId2 = "doc2";
      const contentHash = "dochash";
      const proof = "success";
      const riskScore = 1;
      const sessionId = 1;

      await controller.uploadData(addr1, docId, proof, true);
      await controller.confirm(
        addr1,
        docId,
        contentHash,
        proof,
        sessionId,
        riskScore
      );

      await expect(
        controller.confirm(
          addr1,
          docId2,
          contentHash,
          proof,
          sessionId,
          riskScore
        )
      ).to.be.revertedWith("Controller: session not valid");
    });
  });
});
