from web3 import Web3, middleware
from src.infra.web3 import BaseWeb3
from decimal import Decimal
from eth_account import Account
from eth_account.messages import encode_defunct

class EVMAdapter(BaseWeb3):
    def __init__(self, rpc_url="", mnemonic="", private_key=""):
        self.rpc_url = rpc_url
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.web3.middleware_onion.inject(middleware.geth_poa_middleware, layer=0)
        
        self.account = None
        if not self.web3.is_connected():
            raise Exception("Please check your rpc url")
        if mnemonic:
            self.account = self.web3.eth.account.from_mnemonic(mnemonic)
        elif private_key:
            self.account = self.web3.eth.account.from_key(private_key)
        self.chain_id = self.web3.eth.chain_id

    def generate_new_wallet_address(self) -> (str, str):
        acc = self.web3.eth.account.create()
        address: str = acc.address
        prv_key = self.web3.to_hex(acc.key)
        return address, prv_key
    
    def get_session_with_doc_id(self, doc_id):
        return ""
    
    def submit_gene_data(self, session_id, doc_id, content_hash, proof, risk_score):
        return ""
    
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
    
    def to_json(self, dict):
        return Web3.toJSON(dict)

    def get_tx_info(self, tx_hash):
        return self.web3.eth.get_transaction_receipt(tx_hash)

    def nonce(self, address):
        return self.web3.eth.get_transaction_count(address)

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

    def create_contract_tx(self, to, amount, contract_address, abi):
        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        decimals = contract.functions.decimals().call()
        amount = int(Decimal(str(amount)) * Decimal(10) ** decimals)
        tx = contract.functions.transfer(to, amount).buildTransaction(
            {
                "nonce": self.nonce(self.account.address),
                "from": self.account.address,
                "maxFeePerGas": self.web3.toWei("1.5", "gwei"),
                "maxPriorityFeePerGas": self.web3.toWei("1.5", "gwei"),
                "chainId": self.chain_id,
            }
        )
        tx.update({"gas": self.web3.eth.estimate_gas(tx)})
        return tx

    def send_token(self, to, amount, contract_address, abi):
        if not self.account:
            raise Exception("Please set an account")
        try:
            tx = self.create_contract_tx(to, amount, contract_address, abi)
            signed_tx = self.account.sign_transaction(tx)
            return self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        except Exception as e:
            print(e)

    def from_wei(self, wei, denomination):
        """https://web3py.readthedocs.io/en/stable/examples.html#converting-currency-denominations"""
        return self.web3.fromWei(wei, denomination)

    def to_wei(self, value, denomination):
        """https://web3py.readthedocs.io/en/stable/examples.html#converting-currency-denominations"""
        return self.web3.toWei(value, denomination)

    def from_value(self, value, decimal_places):
        DECIMALS = 10**decimal_places
        return value / DECIMALS

    def get_balance(self, address):
        return self.web3.eth.get_balance(address)

    def get_decimal(self, contract_address, abi):
        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        return contract.functions.decimals().call()

    def get_contract_balance(self, address, contract_address, abi):
        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        balance = contract.functions.balanceOf(address).call()
        decimal_places = contract.functions.decimals().call()
        return self.from_value(balance, decimal_places)
        """
        Scan a **list** of `address` from `start_block` to `end_block`
        """
        new_deposit_txs = defaultdict(list)
        total_blocks = 0
        for block_data in self.scan_blocks(start_block, end_block):
            block_transactions = block_data.transactions
            for tx in block_transactions:
                to_addr = tx.to
                if to_addr in address:
                    print(f"{tx['from']} -> {tx['to']}")
                    new_deposit_txs[to_addr].append(tx)
            total_blocks += 1
        return total_blocks, new_deposit_txs