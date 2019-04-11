from tests.structs.vectorvars import VectorVars
from tests.structs.vectormessage import VectorMessage


class Vector(object):
    def __init__(self, init_vectorvars, resp_vectorvars, handshake_hash, messages):
        """
        :param init_vectorvars:
        :type init_vectorvars: VectorVars
        :param resp_vectorvars:
        :type resp_vectorvars: VectorVars
        :param handshake_hash:
        :type handshake_hash: bytes
        :param messages:
        :type messages: list | tuple
        """
        self._init_vectorvars = init_vectorvars  # type: VectorVars
        self._resp_vectorvars = resp_vectorvars  # type: VectorVars
        self._handshake_hash = handshake_hash  # type: bytes
        self._messages = tuple(messages)  # type: tuple[VectorMessage]

    @property
    def init_vectorvars(self):
        return self._init_vectorvars

    @property
    def resp_vectorvars(self):
        return self._resp_vectorvars

    @property
    def handshake_hash(self):
        return self._handshake_hash

    @property
    def messages(self):
        return self._messages
