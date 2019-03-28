from dissononce.dh.public import PublicKey
from dissononce.dh.private import PrivateKey


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
