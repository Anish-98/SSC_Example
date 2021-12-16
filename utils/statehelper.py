from pyteal import *


class State:
    """
    Wrapper arround state variables for stateful smart contracts
    """

    def __init__(self, name: str):
        self.name = name

    def put(self, value) -> App:
        raise NotImplementedError

    def get(self, value) -> App:
        raise NotImplementedError


class LocalState(State):
    def put(self, value) -> App:
        return App.localPut(Int(0), Bytes(self.name), value)

    def get(self) -> App:
        return App.localGet(Int(0), Bytes(self.name))


class GlobalState(State):
    def put(self, value) -> App:
        return App.globalPut(Bytes(self.name), value)

    def get(self) -> App:
        return App.globalGet(Bytes(self.name))
