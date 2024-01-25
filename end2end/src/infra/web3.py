from abc import ABC, abstractmethod

class BaseWeb3(ABC):

    @abstractmethod
    def generate_new_wallet_address(self):
        """Generate wallet address for user to interact with blockchain"""
        pass

    @abstractmethod
    def sign_message(self, message: str, prv_key: str) -> bytes:
        """Sign message for authenticate"""

    @abstractmethod
    def verify_message(self, message: str, signature: bytes, address: str) -> bool:
        """Verify message signed"""

    @abstractmethod
    def get_session_with_doc_id(self, user_address, doc_id, proof, confirmed):
        """Submit gene id to blockchain and get session id to submit gene data

        Parameters
        ----------
        doc_id: string
            gene id
        """
        pass

    @abstractmethod
    def submit_gene_data(self, user_address, session_id, doc_id, content_hash, proof, risk_score) -> dict:
        """Submit gene data to blockchain with session id

        Parameters
        ----------
        session_id: string
            get from get_session_with_doc_id func
        doc_id: string
            gene id
        content_hash: string
            gene content hashed
        proof: strign
            set any value, currently ignore for demo
        risk_score: number
            [0-3] - Desc: low risk | slightly high risk | high risk | extremely high risk
        """
        pass

