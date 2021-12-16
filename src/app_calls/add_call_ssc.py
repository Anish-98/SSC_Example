import json
from typing import Dict
from algosdk.v2client.algod import AlgodClient
from utils.algo_client import getAlgodClient
from algosdk.future import transaction
from utils.account import Account


def addCall(
    client: AlgodClient, sender: Account, var_a:int, var_b:int, app_id:int
) -> Dict[str, str]:
    """
    Application call to ssc to add two variables 
    """
    withdraw_xet = transaction.ApplicationCallTxn(
        sender=sender.getPublicKey(),
        index=app_id,
        app_args=[b"ADD", var_a.to_bytes(8, "big"),var_b.to_bytes(8,"big")],
        on_complete=transaction.OnComplete.NoOpOC,
        sp=client.suggested_params(),
    )
    stxn = withdraw_xet.sign(sender.getPrivateKey())
    client.send_transaction(stxn)
    txinfo = {
        "on-chain_result": transaction.wait_for_confirmation(client, stxn.get_txid())
    }
    return txinfo


if __name__ == "__main__":
    client = getAlgodClient()
    sender_mn = input()
    sender_ac = Account(sender_mn)
    user_a_var = int(input())
    user_b_var = int(input())
    math_ssc_id = int(input())
    add_result = addCall(client,sender_ac,user_a_var,user_b_var,math_ssc_id)
    print(json(add_result, indent=2))