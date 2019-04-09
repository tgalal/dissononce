from dissononce.dh.x448.public import PublicKey
from dissononce.dh.private import PrivateKey
from dissononce.dh import keypair


class KeyPair(keypair.KeyPair):
    def __init__(self, public_key, private_key):
        super(KeyPair, self).__init__(public_key, private_key)

    @classmethod
    def from_bytes(cls, data):
        """
        :param data:
        :type data: bytes
        :return:
        :rtype: KeyPair
        """
        if len(data) != 112:
            raise ValueError("Wrong length: %d" % len(data))

        return cls(PublicKey(data[56:]), PrivateKey(data[:56]))
