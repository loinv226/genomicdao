from abc import ABC, abstractmethod
from src.type import GeneProfile
class BaseStorage(ABC):

    @abstractmethod
    def save_gene_profile(self, account_id, data: GeneProfile):
        """Save gene data to storage"""
        pass

    @abstractmethod
    def get_gene_profile(self, account_id) -> GeneProfile:
        """Get gene data from storage"""
        pass

    @abstractmethod
    def is_gene_saved(self, gene_id: str) -> bool:
        pass

