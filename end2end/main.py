#!/usr/bin/env python3

from time import sleep
import os
from src.adapter.request import Request
from src.adapter.evm_adapter import EVMAdapter
from src.client.session import SessionController
from src.client.gene import GeneController
from dotenv import load_dotenv
from src import env

def main():
    
    load_dotenv(".env")

    request = Request()
    sessionCtl = SessionController(request)

    print("Hello, this is a simulation of the process of analyzing your gene data that has been saved in the file sample.json")
    print("=====Checking session=====")
    sleep(1)
    sessionCtl.load_session()
    print(f"-> Hello, {sessionCtl.session().account}")
    print(f"-> Done\n")

    print("=====Check profile=====")
    print("-> Checking...")
    sleep(1)
    sessionCtl.fetch_profile_if_need()
    session = sessionCtl.session()
    profile = session.gene_profile
    print(f"-> Done\n")

    bsc_adapter = EVMAdapter()
    geneCtl = GeneController(request, bsc_adapter)

    if not session.is_gene_profile_exist():
        print("=====Upload Gene data=====")
        sleep(1)
        print("-> Uploading...")
        profile = geneCtl.start_upload_process(session.account)
        print(f"-> Done\n")

        if profile is None:
            print("-> Profile empty, exit!")
            return
    
    if not profile.submited_to_blockchain:
        print("=====Sync data to blockchain=====")
        address, prv_key = bsc_adapter.generate_new_wallet_address()
        profile = geneCtl.sync_gene_profile_to_blockchain(session.account, env.SIGN_MESSAGE, address, prv_key)
        print(f"-> Done\n")
        
    print("=====Profile info=====")
    print(f"-> Account: {session.account}")
    print(f"-> Hadhed content: {profile.hashed_content}")
    print(f"-> Gene info: {profile.gene_content}")
    print(f"-> PCSP token: {profile.pcsp_token_amount/10**18}")
    print(f"-> GNFT ID: {profile.gnft_id}")

if __name__ == "__main__":
    main()