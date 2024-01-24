from src.infra.storage import BaseStorage
from src.infra.cipher import BaseCipher
from src.type import GeneProfile

class TEEService:
    """Trusted execution environment service"""

    def __init__(self, storage: BaseStorage, cipher: BaseCipher):
        self.storage = storage
        self.cipher = cipher

    def handle_upload_gene_data(self, account_id: str, data: dict) -> GeneProfile:
        """Handle data upload, compute score and save"""

        gene_id = data.get('gene_id')
        gene_data = data.get('data')
        if gene_id is None or gene_data is None:
            raise Exception("Gene data invalid")
        
        gene_profile = self.storage.get_gene_profile(account_id)
        if gene_profile is not None or self.storage.is_gene_saved(gene_id):
            raise Exception("Gene data used")
        
        return self.__save_gene_data(account_id, gene_id, gene_data)

    def compute_risk_score(self, gene_data: str):
        """Compute PCSP score"""
        match(gene_data.lower()):
            case "low risk":
                return 0
            case "slightly high risk":
                return 1
            case "high risk":
                return 2
            case "extremely high risk":
                return 3
        raise Exception("Gene data not valid")

    def load_gene_profile(self, account_id: str):
        """Load to storage"""
        gene_profile = self.storage.get_gene_profile(account_id)
        if gene_profile is None:
            return
        if gene_profile.decrypted_content:
            return gene_profile
        
        gene_profile.gene_content = self.cipher.decrypt(gene_profile.gene_content)
        gene_profile.decrypted_content = True
        
        return gene_profile

    def __save_gene_data(self, account_id: str, gene_id: str, gene_data: str):
        """Save to storage"""

        risk_score = self.compute_risk_score(gene_data)
        gene_hashed_content = self.cipher.hash(gene_data)
        gene_encrypted_content = self.cipher.encrypt(gene_data)

        new_gene_profile = GeneProfile(id=gene_id,account_id=account_id, gene_content=gene_encrypted_content,
                                        hashed_content=gene_hashed_content, risk_score=risk_score)
        self.storage.save_gene_profile(account_id, new_gene_profile)

        return new_gene_profile