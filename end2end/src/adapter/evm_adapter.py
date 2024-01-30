import os
import json
from web3 import Web3, middleware
from src.infra.web3 import BaseWeb3
from decimal import Decimal
from eth_account import Account
from eth_account.messages import encode_defunct

class EVMAdapter(BaseWeb3):
    def __init__(self):
        rpc_url = os.getenv("EVM_RPC_URL")
        owner_prv_key = os.getenv('CONTRACT_OWNER_PRV')
        self.controller_contract_address = os.getenv('CONTROLLER_CONTRACT_ADDRESS')
        with open("contract_abi.json") as f:
            info_json = json.load(f)
            self.controller_abi = info_json["abi"]

        if rpc_url is None or rpc_url == "":
            raise Exception("RPC URL not config")
        
        self.rpc_url = rpc_url
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.web3.middleware_onion.inject(middleware.geth_poa_middleware, layer=0)
        if not self.web3.is_connected():
            raise Exception("Please check your rpc url")
        
        self.account = None
        if owner_prv_key:
            self.account = self.web3.eth.account.from_key(owner_prv_key)
        self.chain_id = self.web3.eth.chain_id

    def generate_new_wallet_address(self) -> (str, str):
        acc = self.web3.eth.account.create()
        address: str = acc.address
        prv_key = self.web3.to_hex(acc.key)
        return address, prv_key
    
    def sign_message(self, message: str, prv_key: str) -> bytes:
        msg = encode_defunct(text=message)
        signed_message = self.web3.eth.account.sign_message(msg, private_key=prv_key)
        signature = signed_message.signature
        return signature

    def verify_message(self, message: str, signature: bytes, address: str) -> bool:
        msg = encode_defunct(text=message)
        if self.web3.eth.account.recover_message(msg, signature=signature) == address:
            return True
        return False
    
    def submit_gene_data(self, user_address, session_id, doc_id, content_hash, proof, risk_score) -> dict:
        if not self.account:
            raise Exception("Please set an account")
        
        if not self.controller_abi:
            raise Exception("Contract ABI not loaded")
        
        try:
            contract = self.web3.eth.contract(address=self.controller_contract_address, abi=self.controller_abi)
            tx = self.create_submit_tx(contract, user_address, doc_id, content_hash, proof, session_id, risk_score)
            signed_tx = self.account.sign_transaction(tx)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            # call to get session
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            processed_logs = contract.events.UploadSuccess().process_receipt(tx_receipt)
            # print(f"result.items: {processed_logs[0]['args']}")
            if len(processed_logs) == 0:
                return None
            
            return processed_logs[0]['args']
        
        except Exception as e:
            print(f"-> {e}")
    
    def get_session_with_doc_id(self, user_address, doc_id, proof, confirmed):
        if not self.account:
            raise Exception("Please set an account")
        
        if not self.controller_abi:
            raise Exception("Contract ABI not loaded")
        
        try:
            contract = self.web3.eth.contract(address=self.controller_contract_address, abi=self.controller_abi)
            tx = self.create_upload_doc_tx(contract, user_address, doc_id, proof, confirmed)
            signed_tx = self.account.sign_transaction(tx)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
            # call to get session
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            processed_logs = contract.events.UploadData().process_receipt(tx_receipt)
            # print(f"processed_logs: {processed_logs}")
            if len(processed_logs) == 0:
                return None
            
            return processed_logs[0]['args'].get('sessionId')
        
        except Exception as e:
            print(e)
            
    def create_upload_doc_tx(self, contract, user_address, doc_id, proof, confirmed):
        tx = contract.functions.uploadDoc(user_address, doc_id, proof, confirmed).build_transaction(
            {
                "nonce": self.nonce(self.account.address),
                "gasPrice": self.web3.eth.gas_price,
                # "from": self.account.address,
                # "maxFeePerGas": self.web3.toto_weiWei("1.5", "gwei"),
                # "maxPriorityFeePerGas": self.web3.to_wei("1.5", "gwei"),
                # "chainId": self.chain_id,
            }
        )
        # tx.update({"gas": self.web3.eth.estimate_gas(tx)})
        return tx
    
    def create_submit_tx(self, contract, user_address, doc_id, hash_content, proof, session_id, risk_score):
        tx = contract.functions.confirm(user_address, doc_id, hash_content, proof, session_id, risk_score).build_transaction(
            {
                "nonce": self.nonce(self.account.address),
                "gasPrice": self.web3.eth.gas_price,
            }
        )
        return tx
    
    def nonce(self, address):
        return self.web3.eth.get_transaction_count(address)
    
    def to_json(self, dict):
        return Web3.toJSON(dict)

    def get_tx_info(self, tx_hash):
        return self.web3.eth.get_transaction_receipt(tx_hash)

    def send(self, to, amount):
        if not self.account:
            raise Exception("Please set an account")
        try:
            tx = self.create_tx(to, amount)
            signed_tx = self.account.sign_transaction(tx)

            return self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        except Exception as e:
            print(e)
            return e

    def get_fee(self):
        return self.web3.eth.gas_price

    def create_tx(self, to, amount):
        tx = {
            "from": self.account.address,
            "to": self.web3.toChecksumAddress(to),
            "value": self.to_wei(amount, "ether"),
            "nonce": self.nonce(self.account.address),
            "maxFeePerGas": self.web3.toWei("1.5", "gwei"),
            "maxPriorityFeePerGas": self.web3.toWei("1.5", "gwei"),
            "chainId": self.chain_id,
        }
        tx.update({"gas": self.web3.eth.estimate_gas(tx)})
        return tx

    def from_wei(self, wei, denomination):
        return self.web3.from_wei(wei, denomination)

    def to_wei(self, value, denomination):
        return self.web3.to_wei(value, denomination)

    def from_value(self, value, decimal_places):
        DECIMALS = 10**decimal_places
        return value / DECIMALS

    def get_balance(self, address):
        return self.web3.eth.get_balance(address)

    def get_decimal(self, contract_address, abi):
        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        return contract.functions.decimals().call()