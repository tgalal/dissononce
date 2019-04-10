from dissononce.dh.dh import DH
from dissononce.dh.private import PrivateKey


class NoGenDH(DH):
    def __init__(self, dh, privatekey):
        """
        :param dh:
        :type dh: DH
        :param privatekey:
        :type privatekey: PrivateKey
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
