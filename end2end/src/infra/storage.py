from abc import ABC, abstractmethod

class BaseStorage(ABC):

    @abstractmethod
    def save_gene_data(user_id, data):
        """Save gene data to storage"""
        pass

    @abstractmethod
    def get_gene_data(user_id):
        """Get gene data from storage"""
        pass

