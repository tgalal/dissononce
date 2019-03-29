class Vector(object):
    def __init__(self,
                 protocol_name,
                 init_prologue,
                 init_static,
                 init_ephemeral,
                 init_remote_static,
                 resp_prologue,
                 resp_static,
                 resp_ephemeral,
                 handshake_hash
                 ):
        """
        :param protocol_name:
        :type protocol_name:  str
        :param init_prologue:
        :type init_prologue: str
        :param init_static:
        :type init_static: str
        :param init_ephemeral:
        :type init_ephemeral: str
        :param init_remote_static:
        :type init_remote_static: str
        :param resp_prologue:
        :type resp_prologue: str
        :param resp_static:
        :type resp_static: str
        :param resp_ephemeral:
        :type resp_ephemeral: str
        :param handshake_hash:
        :type handshake_hash: str
        """
        self._protocol_name = protocol_name
        self._init_prologue = init_prologue
        self._init_static = init_static
        self._init_ephemeral = init_ephemeral
        self._init_remote_static = init_remote_static
        self._resp_prologue = resp_prologue
        self._resp_static = resp_static
        self._resp_ephemeral = resp_ephemeral
        self._handshake_hash = handshake_hash

    @property
    def protocol_name(self):
        return self._protocol_name

    @property
    def init_prologue(self):
        return self._init_prologue
