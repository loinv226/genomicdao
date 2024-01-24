from abc import ABC, abstractmethod
from src.type import GeneProfile
class BaseNetwork(ABC):

    @abstractmethod
    def register_new_account(self):
        pass

    @abstractmethod
    def fetch_gene_profile(self, account: str):
        pass

    @abstractmethod
    def upload_gene_data(self, account_id: str, data: dict) -> GeneProfile:
        """Upload gene data to server
        
        Return: 
        ----------
        gene_profile: GeneProfile
            gene profile info
        """
        pass

    @abstractmethod
    def sync_gene_profile_to_blockchain(self, account_id: str, message: str, address: str, signature: str):
        "Sync gene info to blockchain after upload"
        pass
