from abc import ABC, abstractmethod

class BaseNetwork(ABC):

    @abstractmethod
    def generate_new_wallet_address():
        """Generate wallet address for user to interact with blockchain"""
        pass

    @abstractmethod
    def get_session_with_doc_id(doc_id):
        """Submit gene id to blockchain and get session id

        Parameters
        ----------
        doc_id: string
            gene id
        """
        pass

    @abstractmethod
    def submit_gene_data(session_id, doc_id, content_hash, proof, risk_score):
        """Submit gene id to blockchain and get session id

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
            [0-3] low risk | slightly high risk | high risk | extremely high risk
        """
        pass

