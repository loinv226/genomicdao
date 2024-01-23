from abc import ABC, abstractmethod

class BaseNetwork(ABC):

    @abstractmethod
    def register_new_account(data):
        """Register account when not exist session"""
        pass

    @abstractmethod
    def upload_gene_data(data):
        """Upload gene data to server

        Parameters
        ----------
        data: binary
            data to upload
        
        Return: 
        ----------
        hash: string
            transaction id
        gene_info: string
            gene info
        gene_hash: string
            to check integrity of gene data
        """
        pass

