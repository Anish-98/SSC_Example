from algosdk import account, mnemonic
import json


def generate_account():
    """
    Function to generate new Algorand Account
    """
    private_key, address = account.generate_account()
    address_mn = mnemonic.from_private_key(private_key)
    account_detail = {"address": address, "mnemonic": address_mn}
    return account_detail


if __name__ == "__main__":

    secrets_file = open("account_secrets.txt", "a")
    secrets_file.write(json.dumps(generate_account(), indent=2) + "\n")
    secrets_file.write("\n")
    print(generate_account())
