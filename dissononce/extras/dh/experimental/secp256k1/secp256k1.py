from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from ecdsa import ellipticcurve
import ecdsa
import hashlib

from .private import PrivateKey
from .public import PublicKey
from dissononce.dh.dh import DH
from dissononce.dh.keypair import KeyPair


class SECP256K1DH(DH):
    def __init__(self):
        super(SECP256K1DH, self).__init__("secp256k1", 32, 33)

    def dh(self, keypair, publickey):
        ecdh = ecdsa.ECDH(curve=ecdsa.SECP256k1)
        ecdh.load_private_key_bytes(keypair.private.data)
        ecdh.load_received_public_key_bytes(publickey.data)

        result = ecdh.public_key.pubkey.point * \
                 ecdh.private_key.privkey.secret_multiplier
        assert(result != ellipticcurve.INFINITY)

        return hashlib.sha256(result.to_bytes(encoding="compressed")).digest()

    def create_public(self, data):
        return PublicKey(data)

    def generate_keypair(self, privatekey=None):
        if privatekey is None:
            private = ec.generate_private_key(ec.SECP256K1())
        else:
            private = ec.derive_private_key(
                    int.from_bytes(privatekey.data, 'big'), ec.SECP256K1())

        public = private.public_key()

        return KeyPair(
            PublicKey(
                public.public_bytes(
                    encoding=serialization.Encoding.X962,
                    format=serialization.PublicFormat.CompressedPoint
                )
            ), PrivateKey(
                private.private_numbers().private_value.to_bytes(32, 'big')
            )
        )
