import requests
from os import path
from time import time
import jsonpickle
from src.infra.network import BaseNetwork
from src.infra.web3 import BaseWeb3
from src.type import GeneProfile

class GeneController:
    __gene_data: dict = None
    __request: BaseNetwork = None

    def __init__(self, request: BaseNetwork, web3: BaseWeb3):
        self.__request = request
        self.__web3 = web3

    def start_upload_process(self, account_id: str):
        gene_file = self.__select_gene_file()
        print(f"gene_file: {gene_file}")
        if not self.__is_file_exist(gene_file):
            raise Exception("Gene file not found")
        
        self.__load_gene_file(gene_file)
        if self.__gene_data is None:
            raise Exception("Gene file not valid")
        
        return self.__submit_gene_data(account_id)
    
    def sync_gene_profile_to_blockchain(self, account_id: str, sign_message: str, address: str, prv_key: str):
        signature = self.__web3.sign_message(sign_message, prv_key)
        gene_profile = self.__request.sync_gene_profile_to_blockchain(account_id, sign_message, address, signature)
        return gene_profile

    def __select_gene_file(self):
        gene_file = input("$ Please enter gene file name? [default: sample.json]: ")
        if gene_file is None or gene_file == "":
            return "sample.json"
        return gene_file

    def __is_file_exist(self, file: str):
        if path.exists(file):
            return True
        return False
    
    def __load_gene_file(self, file: str):
        with open(file, "r") as f:
            data = f.read()
            if data is not None and data != "":
                self.__gene_data = jsonpickle.decode(data);

    def __submit_gene_data(self, account_id: str) -> GeneProfile:
        """Submit gene data to server"""
        
        gene_profile = self.__request.upload_gene_data(account_id, self.__gene_data)
        return gene_profile
    

