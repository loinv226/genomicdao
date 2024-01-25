## Getting started

### Evironments

- Python version: Python 3.10 (3.6+ is fine)
- Node 18.16.0

### Project structure

- `genomicdao/`: Contract sources
- `end2end/`: Application sources
- `end2end/main.py`: Enty script
- `end2end/src`: Components in system (gateway, tee, storage, network request, web3 blockchain)

### Installing

## SMART CONTRACT

- Move into genomicdao folder and install packages: `npm install`
- To test with hardhat local node run: `npm run start:node`
- Create .env file: `cp .env.example .env`
- Compile contracts: `npm run compile`
- Deploy contracts: `npm run deploy`

## Run application:

- Move to end2end folder and install packages: `pip install -r requirements.txt`
- Create .env file: `cp .env.example .env`
- Run application with script `main.py`

## Sample:

sample.json must include following values with format:

```
{
    "gene_id": string,
     "data": low risk | slightly high risk | high risk | extremely high risk
}
```

## Local storage:

use file to store with some data encrypted
