from typing import List, Dict, Any, Union, Tuple
from base64 import b64decode
from utils.algo_client import getAlgodClient
from algosdk.v2client.algod import AlgodClient
import json
from pyteal import compileTeal, Mode, Expr


def fullyCompileContract(client: AlgodClient, contract: Expr) -> bytes:
    """
    Functionality to compile Stateful Smart contract
    """
    teal = compileTeal(contract, mode=Mode.Application, version=5)
    response = client.compile(teal)
    return b64decode(response["result"])


def decodeState(stateArray: List[Any]) -> Dict[bytes, Union[int, str]]:
    state: Dict[str, Union[bytes, str]] = dict()

    for pair in stateArray:
        key = b64decode(pair["key"]).decode("utf-8")

        value = pair["value"]
        valueType = value["type"]

        if valueType == 2:
            # value is uint64
            value = value.get("uint", 0)
        elif valueType == 1:
            # value is byte array
            value = str(b64decode(value.get("bytes", "")))
        else:
            raise Exception(f"Unexpected state type: {valueType}")

        state[key] = value

    return state


def getAppGlobalState(
    client: AlgodClient, appID: int
) -> Dict[bytes, Union[int, bytes]]:
    """
    Functionality to query global state of any stateful smart contract
    """
    appInfo = client.application_info(appID)
    return decodeState(appInfo["params"]["global-state"])


def getAppLocalState(
    client: AlgodClient, addr: str, app_id: int
) -> Dict[bytes, Union[int, bytes]]:
    """
    Functionality to query local state of any user opted into stateful smart contract

    """
    result = client.account_info(addr)
    for local_state in result["apps-local-state"]:
        if local_state["id"] == app_id:
            if "key-value" in local_state:
                return decodeState(local_state["key-value"])


def getBalances(client: AlgodClient, account: str) -> Dict[int, int]:
    """
    functionality to query algo balance of an account
    """
    balances: Dict[int, int] = dict()

    accountInfo = client.account_info(account)

    # set key 0 to Algo balance
    balances[0] = accountInfo["amount"]

    assets: List[Dict[str, Any]] = accountInfo.get("assets", [])
    for assetHolding in assets:
        assetID = assetHolding["asset-id"]
        amount = assetHolding["amount"]
        balances[assetID] = amount

    return balances


def getLastBlockTimestamp(client: AlgodClient) -> Tuple[int, int]:
    """
    Functionality to get latest block timestamp from testnet
    """
    status = client.status()
    lastRound = status["last-round"]
    block = client.block_info(lastRound)
    timestamp = block["block"]["ts"]
    return timestamp


def print_asset_holding(algodclient, account, assetid):
    """
    Functionality to query particular asset holding of an account
    """
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info["assets"]:
        scrutinized_asset = account_info["assets"][idx]
        idx = idx + 1
        if scrutinized_asset["asset-id"] == assetid:
            print("Asset ID: {}".format(scrutinized_asset["asset-id"]))
            print(json.dumps(scrutinized_asset, indent=4))
            break


if __name__ == "__main__":
    info = getAppLocalState(
        client=getAlgodClient(),
        addr="T77B5WWN2AOUPJ4JKYYBYCYMSC5Q2STODEMEB2L5WIFDGEFFH7CKBCUUYE",
        app_id=21336826,
    )
    print(info)

    info_global = getAppGlobalState(client=getAlgodClient(), appID=46852009)
    print(info_global)
