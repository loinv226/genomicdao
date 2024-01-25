class GeneProfile:
    id: str = None
    account_id: str = None
    hashed_content: str = None
    gene_content: str = None
    risk_score: int = None
    address: str = None
    pcsp_token_amount = 0
    gnft_id: str = None
    submited_to_blockchain = False
    decrypted_content = False

    def __str__(self) -> str:
        return f"id: {self.id} - account_id: {self.account_id} - hashed_content: {self.hashed_content}"
    
    def __init__(self, id: str, account_id: str, gene_content: str, hashed_content: str, risk_score: int):
        self.id = id
        self.account_id = account_id
        self.gene_content = gene_content
        self.hashed_content = hashed_content
        self.risk_score = risk_score
        
class Wallet:
    address = ""
    prv_key = ""

class Session:
    account = None
    gene_profile: GeneProfile = None
    wallet: Wallet = None

    def __str__(self) -> str:
        return str(self.account)
    
    def is_gene_profile_exist(self):
        return self.gene_profile is not None and self.gene_profile.hashed_content is not None and self.gene_profile.hashed_content != ""