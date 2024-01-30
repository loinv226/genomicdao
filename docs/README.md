# Blockchain engineer assignment

## Table of contents
* [Description](#description)
* [Components](#components)
* [Instruction](#instruction)
* [How to run it](#how-to-run-it)
* [File structure](#file-structure)
 
## Description
GenomicDAO is an AI-Powered DeSci Platform for Precision Medicine. PCSP (Post-Covid Stroke Prevention), the first released token on GenomicDAO platform, allows users to purchase genetic testing services and to govern the drug discovery and development for stroke.

### User flow
![E2E flow](./images/end-user-flow.jpg?raw=true "e2e flow")

1. After the registered user purchases G-Stroke service, the saliva sample will be collected for genetic decoding. User’s gene data is encrypted and securely stored in the system.
2. All the computation on the user’s gene data is executed in a TEE (Trusted execution environment) where the computation cannot be tampered with and the intermediate stages of a computation cannot be read by not-a-computer.
3. The result of the computation process is the genetic insights which will be used to generate a full report for the user.
4. According to the stroke risk score, the user will be received amount of PCSP token corresponding to the following:
   - extremely high risk: 15000 PCSP 
   - high risk: 3000 PCSP 
   - slightly high risk: 225 PCSP 
   - normal or low risk: 30 PCSP
5. At the same time, the user receives a G-NFT, which is minted on the blockchain based on the user's gene data. This NFT defines the ownership of the gene profile.

## Components

![Components](./images/components.jpg?raw=true "Components")


### Blockchain
The following main functions need to be implemented:
- Submit gene data
- Mint G-NFT
- Reward PCSP

Those features should be implemented with contracts on layer 2 built with OP Stack. For more information:
- [OP Stack](https://stack.optimism.io/#)


## Instructions
To complete this assignment you should implement the `/// TODO:` with solution code. Most of the changes will be in `/contracts/`

- Contracts:
    - NFT.sol: for GeneNFT
    - Token.sol: for PCSP Token
    - Storage.sol: for managing the document info on-chain

- Blockchain event when:
   - Gene data is submitted
   - GNFT is minted
   - PCSP is rewarded

### Run the test
Requirements
- [Node](https://nodejs.org/en)

Go to folder `/genomicdao/` and run the following command to install package requirements
```
npm install
```

To run the test
```
npx hardhat test
```



## How to run it
Build OP Stack Rollups. For more information [Optimism docs](https://stack.optimism.io/docs/build/getting-started/)

### Build the optimism

Clone source code

```
git clone https://github.com/ethereum-optimism/optimism.git
```

Build packages
```
cd optimism

pnpm install
make op-node op-batcher op-proposer
pnpm build
```

### Build op-geth

Clone source code
```
cd ~
git clone https://github.com/ethereum-optimism/op-geth.git
```

Build from source code
```
cd op-geth
make geth
```


### Preapre accounts

- The `Admin` account which has the ability to upgrade contracts.
- The `Batcher` account which publishes Sequencer transaction data to L1.
- The `Proposer` account which publishes L2 transaction results to L1.
- The `Sequencer` account which signs blocks on the p2p network.

Also, fund these accounts some test ETH for running.

### Run the node software

#### op-geth
```
cd ~/op-geth

./build/bin/geth \
        --datadir ./datadir \
        --http \
        --http.corsdomain="*" \
        --http.vhosts="*" \
        --http.addr=0.0.0.0 \
        --http.api=web3,debug,eth,txpool,net,engine \
        --ws \
        --ws.addr=0.0.0.0 \
        --ws.port=8546 \
        --ws.origins="*" \
        --ws.api=debug,eth,txpool,net,engine \
        --syncmode=full \
        --gcmode=archive \
        --nodiscover \
        --maxpeers=0 \
        --networkid=42069 \
        --authrpc.vhosts="*" \
        --authrpc.addr=0.0.0.0 \
        --authrpc.port=8551 \
        --authrpc.jwtsecret=./jwt.txt \
        --rollup.disabletxpoolgossip=true
```

#### op-node
```
cd ~/optimism/op-node

./bin/op-node \
	--l2=http://localhost:8551 \
	--l2.jwt-secret=./jwt.txt \    
	--sequencer.enabled \
	--sequencer.l1-confs=3 \
	--verifier.l1-confs=3 \
	--rollup.config=./rollup.json \
	--rpc.addr=0.0.0.0 \
	--rpc.port=8547 \
	--p2p.disable \
	--rpc.enable-admin \
	--p2p.sequencer.key=$SEQ_KEY \
	--l1=$L1_RPC \
	--l1.rpckind=$RPC_KIND
```

#### op-batcher
```
cd ~/optimism/op-batcher

./bin/op-batcher \
    --l2-eth-rpc=http://localhost:8545 \
    --rollup-rpc=http://localhost:8547 \
    --poll-interval=1s \
    --sub-safety-margin=6 \
    --num-confirmations=1 \
    --safe-abort-nonce-too-low-count=3 \
    --resubmission-timeout=30s \
    --rpc.addr=0.0.0.0 \
    --rpc.port=8548 \
    --rpc.enable-admin \
    --max-channel-duration=1 \
    --l1-eth-rpc=$L1_RPC \
    --private-key=$BATCHER_KEY
```

#### op-proposer
```
cd ~/optimism/op-proposer

./bin/op-proposer \
    --poll-interval=12s \
    --rpc.port=8560 \
    --rollup-rpc=http://localhost:8547 \
    --l2oo-address=$L2OO_ADDR \
    --private-key=$PROPOSER_KEY \
    --l1-eth-rpc=$L1_RPC
```


## File structure
```
genomicdao/                 # Directory contains main
│   
├── contracts/                          
│   ├── NFT.sol
│   ├── Token.sol
│   ├── Storage.sol
│   
├── scripts
│   ├── deploy.js
└── ...
```

