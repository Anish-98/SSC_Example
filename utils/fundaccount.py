from utils.account import Account
from utils.algo_client import getAlgodClient, AlgodClient
from utils.SSC_utils import getBalances
from algosdk.future import transaction


def fundAlgosToAc(client: AlgodClient, receiver: str):
    """
    Functionality to fund any account with 10 Algos
    """
    amt = 10_000_000
    sender_mn = "check chuckle maid average harsh peasant require bonus call video absorb shell express glance mosquito ethics fire knee switch private pledge cage emerge abandon tunnel"
    sender_ac = Account(sender_mn)

    fundalgosTxn = transaction.PaymentTxn(
        sender=sender_ac.getPublicKey(),
        sp=client.suggested_params(),
        receiver=receiver,
        amt=amt,
    )
    stxn = fundalgosTxn.sign(sender_ac.getPrivateKey())
    txid = client.send_transaction(stxn)
    txinfo = transaction.wait_for_confirmation(client, txid)
    return txinfo


if __name__ == "__main__":
    client = getAlgodClient()
    receiver = str(input())
    txinfo = fundAlgosToAc(client, receiver)
    getBalances(client, receiver)
    print(txinfo)
