from dissononce.dh.dh import DH


class NoGenDH(DH):
    """A ```NoGenDH``` wraps an existing ```DH``` object, but disables keypairs generation functionality by fixing all
    generated  keypairs to a single value determined by the```PrivateKey``` passed to it at construction.
    This is used in tests where ephemeral values from test vectors must be used."""
    def __init__(self, dh, privatekey):
        """
        :param dh:
        :type dh: DH
        :param privatekey:
        :type privatekey: dissononce.dh.private.PrivateKey
        """
        super(NoGenDH, self).__init__(dh.name, dh.dhlen)
        self._dh = dh
        self._privatekey = privatekey

    def dh(self, key_pair, public_key):
        return self._dh.dh(key_pair, public_key)

    def create_public(self, data):
        return self._dh.create_public(data)

    def generate_keypair(self, privatekey=None):
        return self._dh.generate_keypair(privatekey or self._privatekey)
