from src.type import GeneProfile
from src.adapter.evm_adapter import EVMAdapter
from src.adapter.storage import LocalStorage
from src.adapter.cipher import Cipher
from src.tee import TEEService
from src import env

class Gateway:
    
    def __init__(self):
        self.bsc_adapter = EVMAdapter(rpc_url=env.EVM_RPC_URL)
        self.local_storage = LocalStorage()
        cipher = Cipher()
        self.tee_service = TEEService(self.local_storage, cipher)

    def get_profile(self, account_id: str):
        gene_profile = self.tee_service.load_gene_profile(account_id)
        return gene_profile

    def handle_upload_gene_data(self, account_id: str, data: dict):
        gene_profile = self.tee_service.handle_upload_gene_data(account_id, data)
        return gene_profile

    def sync_gene_profile_to_blockchain(self, account_id: str, message: str, address: str, signature: str):
        gene_profile = self.tee_service.load_gene_profile(account_id)
        if gene_profile is None:
            raise Exception("Gene profile not upload")
        if gene_profile.submited_to_blockchain == True:
            raise Exception("Gene profile submited to blockchain")
        
        is_owner = self.bsc_adapter.verify_message(message, signature, address)
        if not is_owner:
            raise Exception("Signature invalid")
        
        doc_id = gene_profile.id
        # Get session id to call submit gene data
        session_id = self.bsc_adapter.get_session_with_doc_id(doc_id)
        # Submit
        self.bsc_adapter.submit_gene_data(session_id, doc_id, gene_profile.hashed_content, gene_profile.risk_score)
        # Get total token mined and NFT info
        return gene_profile
    
    
    

