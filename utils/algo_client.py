from algosdk.v2client.algod import AlgodClient

ALGOD_ADDRESS = "https://testnet-algorand.api.purestake.io/ps2"
ALGOD_TOKEN = "UTXD5Nic4t2wr0pAO7Dmc1noR3Vh6kLo7CvI5Dhr"
headers = {
    "X-API-Key": ALGOD_TOKEN,
}


def getAlgodClient() -> AlgodClient:
    return AlgodClient(
        algod_token=ALGOD_TOKEN, algod_address=ALGOD_ADDRESS, headers=headers
    )
