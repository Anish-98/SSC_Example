import json
from typing import Dict
from algosdk.v2client.algod import AlgodClient
from utils.algo_client import getAlgodClient
from algosdk.future import transaction
from utils.account import Account


def user_optin(client: AlgodClient, app_id: int, sender: Account) -> Dict[str, str]:
    """
    optin txn from user to opt in to
    Crowd Funding contract.
    """
    txn = transaction.ApplicationOptInTxn(
        sender=sender.getPublicKey(),
        index=app_id,
        sp=client.suggested_params(),
    )
    signedTransaction = txn.sign(sender.getPrivateKey())
    client.send_transaction(signedTransaction)
    txinfo = {
        "user_optin_info": transaction.wait_for_confirmation(
            client, signedTransaction.get_txid()
        )
    }

    return txinfo


if __name__ == "__main__":
    client = getAlgodClient()
    sender_mn = input()
    sender_ac = Account(sender_mn)
    app_id = int(input())
    user_optin_info = user_optin(client, app_id, sender_ac)
    print(json.dumps(user_optin_info, indent=2))