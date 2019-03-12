from dissononce.dh.key_public import PublicKey
from dissononce.dh.key_private import PrivateKey
from dissononce.util.byte import ByteUtil


class KeyPair(object):
    def __init__(self, public_key, private_key):
        """

        :param public_key:
        :type public_key: PublicKey
        :param private_key:
        :type private_key: PrivateKey
        """
        self._public_key = public_key
        self._private_key = private_key

    @classmethod
    def from_bytes(cls, data):
        """
        :param data:
        :type data: bytes
        :return:
        :rtype: KeyPair
        """
        if len(data) != 64:
            raise ValueError("Wrong length: %d" % len(data))

        dissected = ByteUtil.split(data, 32, 32)
        return cls(PublicKey(dissected[1]), PrivateKey(dissected[0]))

    @property
    def public(self):
        """
        :return:
        :rtype: PublicKey
        """
        return self._public_key

    @property
    def private(self):
        """
        :return:
        :rtype: PrivateKey
        """
        return self._private_key
