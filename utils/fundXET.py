from utils.algo_client import getAlgodClient, AlgodClient
from algosdk.future import transaction
from utils.account import Account

global SENDER_MN
global SENDER_AC

SENDER_MN = "wrestle rescue bird direct vote index office candy upon vital come hockey rapid quarter wash bulb shadow sheriff wreck believe lizard bargain left absent donor"
SENDER_AC = Account(SENDER_MN)


def fundXET(client: AlgodClient, receiver: Account):
    """
    Functionality to fund account with 1000 dummy XETs

    """
    amount = 1000_000_000_000
    xet_id = 47005985
    xet_opt_in = transaction.AssetTransferTxn(
        sender=receiver.getPublicKey(),
        sp=client.suggested_params(),
        receiver=receiver.getPublicKey(),
        amt=0,
        index=xet_id,
    )
    fund_xet_txn = transaction.AssetTransferTxn(
        sender=SENDER_AC.getPublicKey(),
        sp=client.suggested_params(),
        receiver=receiver.getPublicKey(),
        index=xet_id,
        amt=amount,
    )
    transaction.assign_group_id([xet_opt_in, fund_xet_txn])
    signed_optin_txn = xet_opt_in.sign(receiver.getPrivateKey())
    signed_fundXET_txn = fund_xet_txn.sign(SENDER_AC.getPrivateKey())
    client.send_transactions([signed_optin_txn, signed_fundXET_txn])

    txinfo = {
        "fund_xet_txn": transaction.wait_for_confirmation(
            client, signed_fundXET_txn.get_txid()
        )
    }
    return txinfo


def fund_xet_to_contract(client: AlgodClient, receiver: str):
    amount = 1000_000_000_000
    xet_id = 47005985
    fund_to_contract_txn = transaction.AssetTransferTxn(
        sender=SENDER_AC.getPublicKey(),
        receiver=receiver,
        amt=amount,
        index=xet_id,
        sp=client.suggested_params(),
    )
    stxn = fund_to_contract_txn.sign(SENDER_AC.getPrivateKey())
    client.send_transaction(stxn)
    txinfo = {
        "xet_to_contract": transaction.wait_for_confirmation(client, stxn.get_txid())
    }
    return txinfo


if __name__ == "__main__":
    client = getAlgodClient()
    # receiver_mn = input("Enter your Mnemonic: ")
    # receiver_ac = Account(receiver_mn)
    receiver = input()
    fundtxinfo = fund_xet_to_contract(client, receiver)
    print(fundtxinfo)
