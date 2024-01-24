import os.path
from src.infra.storage import BaseStorage
import jsonpickle
from src.type import GeneProfile

class LocalStorage(BaseStorage):
    __storage_path = "local_storage.json"
    __profiles: dict = {}
    __uploaded_genes: dict = {}

    def __init__(self):
        if not os.path.exists(self.__storage_path):
            return
        
        with open(self.__storage_path, "r") as f:
            data = f.read()
            if data is not None and data != "":
                self.__profiles = jsonpickle.decode(data)
                # cache gene uploaded
                self.__uploaded_genes = {value.id: value.account_id for value in self.__profiles.values()}

    def save_gene_profile(self, account_id: str, data: GeneProfile):
        """Save gene data to storage"""

        if account_id is None or data is None:
            raise Exception("Data is empty")
        
        self.__profiles[account_id] = data
        with open(self.__storage_path, 'w') as f:
            f.write(jsonpickle.dumps(self.__profiles))

    def get_gene_profile(self, account_id: str) -> GeneProfile:
        """Get gene data from storage"""
        
        if self.__profiles.get(account_id) is not None:
            return self.__profiles.get(account_id)

    def is_gene_saved(self, gene_id: str):
        if gene_id is None or gene_id == "":
            raise Exception("Gene id is empty")
        return self.__uploaded_genes.get(gene_id) is not None
        