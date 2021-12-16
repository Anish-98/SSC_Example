from typing import Tuple
from algosdk.v2client.algod import AlgodClient
from utils.algo_client import getAlgodClient
from algosdk.future import transaction
from algosdk.logic import get_application_address
from utils.account import Account
from src.contracts.math_ssc import(
  approval_program,
  clear_state_program
)
from utils.SSC_utils import fullyCompileContract


APPROVAL_PROGRAM = b""
CLEAR_STATE_PROGRAM = b""


def getContracts(client: AlgodClient) -> Tuple[bytes, bytes]:
    global APPROVAL_PROGRAM
    global CLEAR_STATE_PROGRAM

    if len(APPROVAL_PROGRAM) == 0:
        APPROVAL_PROGRAM = fullyCompileContract(client, approval_program())
        CLEAR_STATE_PROGRAM = fullyCompileContract(client, clear_state_program())

    return APPROVAL_PROGRAM, CLEAR_STATE_PROGRAM


def createMathContract(
    client: AlgodClient,
    sender: Account,
) -> int:
    approval, clear = getContracts(client)
    globalSchema = transaction.StateSchema(num_uints=4, num_byte_slices=0)
    localSchema = transaction.StateSchema(num_uints=1, num_byte_slices=0)
    app_args=[]
    txn = transaction.ApplicationCreateTxn(
        sender=sender.getPublicKey(),
        on_complete=transaction.OnComplete.NoOpOC,
        approval_program=approval,
        clear_program=clear,
        global_schema=globalSchema,
        local_schema=localSchema,
        app_args=app_args,
        sp=client.suggested_params(),
    )

    signedTransaction = txn.sign(sender.getPrivateKey())
    client.send_transaction(signedTransaction)
    transaction.wait_for_confirmation(client, signedTransaction.get_txid())
    transaction_response = client.pending_transaction_info(signedTransaction.get_txid())
    app_id = transaction_response["application-index"]
    return app_id


if __name__ == "__main__":
    client = getAlgodClient()
    contract_deployer = "want wagon tennis stereo burden order maple increase mail oppose muffin output symptom month story tag option surface chimney trust vault save throw ability prefer"
    deployer_ac = Account(contract_deployer)
    math_ssc_appid = createMathContract(getAlgodClient(),deployer_ac)
    print(math_ssc_appid)

    # If you want to set any global states at the time of deployment ,
    # user_input_a = int(input())
    # user_input_b = int(input())
