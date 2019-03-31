from dissononce.dh.public import PublicKey


class DH(object):
    def __init__(self, name, dhlen):
        self._name = name
        self._dhlen = dhlen

    @property
    def name(self):
        """
        :return:
        :rtype: str
        """
        return self._name

    @property
    def dhlen(self):
        return self._dhlen

    def generate_keypair(self, privatekey=None):
        """
        Generates a new Diffie-Hellman key pair. A DH key pair consists of public_key and private_key elements.
        A public_key represents an encoding of a DH public key into a byte sequence of length DHLEN.
        The public_key encoding details are specific to each set of DH functions.
        :param privatekey:
        :type privatekey: dissononce.dh.private.PrivateKey | None
        :return:
        :rtype: dissononce.dh.keypair.KeyPair
        """

    def create_public(self, data):
        """
        :type data: bytes
        :return:
        :rtype: dissononce.dh.public.PublicKey
        """
        raise PublicKey(data, self.dhlen)

    def dh(self, key_pair, public_key):
        """
        Performs a Diffie-Hellman calculation between the private key in key_pair and the public_key and returns an
        output sequence of bytes of length DHLEN

        :param key_pair:
        :type key_pair: dissononce.dh.keypair.KeyPair
        :param public_key:
        :type public_key: dissononce.dh.public.PublicKey
        :return:
        :rtype: bytes
        """
