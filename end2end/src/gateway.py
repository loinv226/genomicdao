import os
from src.type import GeneProfile
from src.adapter.evm_adapter import EVMAdapter
from src.adapter.storage import LocalStorage
from src.adapter.cipher import Cipher
from src.tee import TEEService
from src import env

class Gateway:
    
    def __init__(self):
        self.bsc_adapter = EVMAdapter()
        
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
        proof = "success"
        # Get session id to call submit gene data
        session_id = self.bsc_adapter.get_session_with_doc_id(address, doc_id, proof, True)
        print(f"-> session_id: {session_id}")
        # Submit
        if session_id is None:
            return gene_profile
        
        info: dict = self.bsc_adapter.submit_gene_data(address, session_id, doc_id, gene_profile.hashed_content, proof, gene_profile.risk_score)
        # Get total token mined and NFT info
        gene_profile.pcsp_token_amount = info.get("tokenAmount")
        gene_profile.gnft_id = info.get("nftId")
        gene_profile.submited_to_blockchain = True
        self.local_storage.save_gene_profile(account_id, gene_profile)

        return gene_profile
    
    
    

