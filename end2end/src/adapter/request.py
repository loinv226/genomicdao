import random
from src.infra.network import BaseNetwork
from src.gateway import Gateway
from src.type import GeneProfile

class Request(BaseNetwork):

    def __init__(self):
        self.gateway = Gateway()

    def register_new_account(self):
        return str(random.getrandbits(32))
    
    def fetch_gene_profile(self, account_id):
        return self.gateway.get_profile(account_id)

    def upload_gene_data(self, account_id: str, data: dict) -> GeneProfile:
        """Upload gene data to server"""
        
        return self.gateway.handle_upload_gene_data(account_id, data)
    
    def sync_gene_profile_to_blockchain(self, account_id: str, message: str, address: str, signature: str):
        "Sync gene info to blockchain after upload"

        return self.gateway.sync_gene_profile_to_blockchain(account_id, message, address, signature)