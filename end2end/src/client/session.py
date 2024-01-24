from os import path
from time import time
import jsonpickle
from src.infra.network import BaseNetwork
from src.type import Session

class SessionController:
     
    __session_file = "client_session.json"
    __session: Session = Session()
    __request: BaseNetwork = None

    def __init__(self, request: BaseNetwork):
        self.__request = request

    def session(self):
        return self.__session
    
    def load_session(self):
        if self.__is_session_file_exist():
            self.__read_and_fill_session()
            print(self.__session)

            if self.__session.account is not None:
                return self.__session
            
        account = self.__generate_new_account()
        self.__validate_account(account)

        self.__session.account = account
        self.__save_session()
        return self.__session
    
    def fetch_profile_if_need(self):
        if self.__session.is_gene_profile_exist():
            return
        
        account = self.__session.account
        if account is None or account == "":
            raise Exception("Account not exist")
        
        gene_profile = self.__request.fetch_gene_profile(account)
        if gene_profile is None:
            return
        
        self.__session.gene_profile = gene_profile
        # not save for privacy or must todo more
        # self.__save_session()

    def __is_session_file_exist(self):
        if path.exists(self.__session_file):
            return True
        return False

    def __read_and_fill_session(self):
        with open(self.__session_file, "r") as f:
            data = f.read()
            if data is not None and data != "":
                self.__session = jsonpickle.decode(data);
        
    def __generate_new_account(self):
        return self.__request.register_new_account()

    def __validate_account(self, account):
        if not account:
            raise Exception("Account not exist")
        if type(account) is not str:
            raise Exception("Account must use string")

    def __save_session(self):
        if not self.__session.account:
            raise Exception("Session is empty")
        
        with open(self.__session_file, 'w') as f:
            f.write(jsonpickle.dumps(self.__session))
