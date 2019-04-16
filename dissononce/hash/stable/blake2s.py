from dissononce.hash.hash import Hash

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hmac import HMAC


class Blake2sHash(Hash):
    def __init__(self):
        super(Blake2sHash, self).__init__("BLAKE2s", 32, 64)

    def hash(self, data):
        digest = hashes.Hash(hashes.BLAKE2s(32), backend=default_backend())
        digest.update(data)
        return digest.finalize()

    def hmac_hash(self, key, data):
        hmac = HMAC(key=key, algorithm=hashes.BLAKE2s(32), backend=default_backend())
        hmac.update(data=data)
        return hmac.finalize()
