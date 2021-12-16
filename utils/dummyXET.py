import json
from utils.algo_client import getAlgodClient
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn


def wait_for_confirmation(client, txid):
    last_round = client.status().get("last-round")
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get("confirmed-round") and txinfo.get("confirmed-round") > 0):
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    return txinfo


def print_created_asset(algodclient, account, assetid):
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info["created-assets"]:
        scrutinized_asset = account_info["created-assets"][idx]
        idx = idx + 1
        if scrutinized_asset["index"] == assetid:
            print("Asset ID: {}".format(scrutinized_asset["index"]))
            print(json.dumps(my_account_info["params"], indent=4))
            break


def print_asset_holding(algodclient, account, assetid):
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info["assets"]:
        scrutinized_asset = account_info["assets"][idx]
        idx = idx + 1
        if scrutinized_asset["asset-id"] == assetid:
            print("Asset ID: {}".format(scrutinized_asset["asset-id"]))
            print(json.dumps(scrutinized_asset, indent=4))
            break


def createASA(algod_client, creator, creator_sk):
    params = algod_client.suggested_params()
    params.fee = 1000
    params.flat_fee = True
    txn = AssetConfigTxn(
        sender=creator,
        sp=params,
        total=4000000000000000000,
        unit_name="txets",
        asset_name="TXETM",
        manager=creator,
        strict_empty_address_check=False,
        url="http://testxetforlaunchpad.com",
        decimals=9,
    )
    stxn = txn.sign(creator_sk)
    txid = algod_client.send_transaction(stxn)
    wait_for_confirmation(algod_client, txid)
    return txid


creator_mnemonic = "wrestle rescue bird direct vote index office candy upon vital come hockey rapid quarter wash bulb shadow sheriff wreck believe lizard bargain left absent donor"
algod_client = getAlgodClient()
creator = mnemonic.to_public_key(creator_mnemonic)
creator_sk = mnemonic.to_private_key(creator_mnemonic)

creation_txid = createASA(algod_client, creator, creator_sk)
ptx = algod_client.pending_transaction_info(creation_txid)
asa_id = ptx["asset-index"]
print_created_asset(algod_client, creator, asa_id)
print_asset_holding(algod_client, creator, asa_id)
