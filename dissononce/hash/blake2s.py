from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hmac import HMAC

from dissononce.hash.hash import Hash


class Blake2sHash(Hash):
    def __init__(self):
        super(Blake2sHash, self).__init__("BLAKE2s")

    def hash(self, data):
        digest = hashes.Hash(hashes.BLAKE2s(32), backend=default_backend())
        digest.update(data)
        return digest.finalize()

    def hashlen(self):
        return 32

    def hmac_hash(self, key, data):
        hmac = HMAC(key=key, algorithm=hashes.BLAKE2s(32), backend=default_backend())
        hmac.update(data=data)
        return hmac.finalize()
