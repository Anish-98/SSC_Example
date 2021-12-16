from algosdk.v2client.algod import AlgodClient
from utils.algo_client import getAlgodClient
from algosdk.future import transaction
from utils.account import Account


def deleteApp(client: AlgodClient, app_id: int, sender: Account) -> None:
    """
    Functionality to delete stateful smart contract
    """
    txn = transaction.ApplicationDeleteTxn(
        sender=sender.getPublicKey(), sp=client.suggested_params(), index=app_id
    )
    signedTransaction = txn.sign(sender.getPrivateKey())
    client.send_transaction(signedTransaction)
    txinfo = transaction.wait_for_confirmation(client, signedTransaction.get_txid())

    return txinfo


if __name__ == "__main__":
    client = getAlgodClient()
    sender_mn = "apart tube distance royal sense random essence sweet proof round clutch cannon skate asthma hover rule label found game inspire blouse connect cement ability ice"
    sender_ac = Account(sender_mn)
    app_id = int(input("Delete App_id: "))
    repsonse = deleteApp(client, app_id, sender_ac)
    print(repsonse)
