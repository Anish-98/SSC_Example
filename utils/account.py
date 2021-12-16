from algosdk import account, mnemonic


class Account:
    def __init__(self, user_mnemonic: str) -> None:
        self.address = mnemonic.to_public_key(user_mnemonic)
        self.sk = mnemonic.to_private_key(user_mnemonic)

    def getPublicKey(self) -> str:
        return self.address

    def getPrivateKey(self) -> str:
        return self.sk


if __name__ == "__main__":
    user = Account(
        "case undo inch music fury tragic blossom vast garage bacon trial impose above culture winner vault visa sword slush unable disease suspect company absent broken"
    )
    user_address = user.getPublicKey()
    user_sk = user.getPrivateKey()
    print(len(user_address))
