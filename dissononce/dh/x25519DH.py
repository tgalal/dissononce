from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization

from dissononce.dh.dh import DH
from dissononce.dh.key_private import PrivateKey
from dissononce.dh.key_public import PublicKey
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

    def generate_keypair(self):
        private = x25519.X25519PrivateKey.generate()
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