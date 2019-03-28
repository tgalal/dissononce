from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization

from dissononce.dh.dh import DH
from dissononce.dh.private import PrivateKey
from dissononce.dh.x25519.public import PublicKey
from dissononce.dh.keypair import KeyPair


class X25519DH(DH):
    def __init__(self):
        super(X25519DH, self).__init__("25519", 32)

    def dh(self, key_pair, public_key):
        """
        :param key_pair:
        :type key_pair: KeyPair
        :param public_key:
        :type public_key: PublicKey
        :return:
        :rtype: bytes
        """
        return x25519.X25519PrivateKey.from_private_bytes(
            key_pair.private.data
        ).exchange(
            x25519.X25519PublicKey.from_public_bytes(
                public_key.data
            )
        )

    def create_public(self, data):
        return PublicKey(data)

    def generate_keypair(self, privatekey = None):
        if privatekey is None:
            private = x25519.X25519PrivateKey.generate()
        else:
            private = x25519.X25519PrivateKey.from_private_bytes(privatekey.data)

        public = private.public_key()

        return KeyPair (
            PublicKey(
                public.public_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PublicFormat.Raw
                )
            ),
            PrivateKey(
                private.private_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PrivateFormat.Raw,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )
        )