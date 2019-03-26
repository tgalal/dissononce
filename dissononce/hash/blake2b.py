from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hmac import HMAC

from dissononce.hash.hash import Hash


class Blake2bHash(Hash):
    def __init__(self):
        super(Blake2bHash, self).__init__("BLAKE2b")

    def hash(self, data):
        digest = hashes.Hash(hashes.BLAKE2b(64), backend=default_backend())
        digest.update(data)
        return digest.finalize()

    def hashlen(self):
        return 64

    def hmac_hash(self, key, data):
        hmac = HMAC(key=key, algorithm=hashes.BLAKE2b(64), backend=default_backend())
        hmac.update(data=data)
        return hmac.finalize()
