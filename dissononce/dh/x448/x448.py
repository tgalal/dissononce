from dissononce.dh.dh import DH
from dissononce.dh.private import PrivateKey
from dissononce.dh.x448.public import PublicKey
from dissononce.dh.keypair import KeyPair

from cryptography.hazmat.primitives.asymmetric import x448
from cryptography.hazmat.primitives import serialization


class X448DH(DH):
    def __init__(self):
        super(X448DH, self).__init__("448", 56)

    def dh(self, keypair, publickey):
        return x448.X448PrivateKey.from_private_bytes(
            keypair.private.data
        ).exchange(
            x448.X448PublicKey.from_public_bytes(
                publickey.data
            )
        )

    def create_public(self, data):
        return PublicKey(data)

    def generate_keypair(self, privatekey=None):
        if privatekey is None:
            private = x448.X448PrivateKey.generate()
        else:
            private = x448.X448PrivateKey.from_private_bytes(privatekey.data)

        public = private.public_key()

        return KeyPair(
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
