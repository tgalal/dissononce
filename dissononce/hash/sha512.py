from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hmac import HMAC

from dissononce.hash.hash import Hash


class SHA512Hash(Hash):
    def __init__(self):
        super(SHA512Hash, self).__init__("SHA512")

    def hash(self, data):
        digest = hashes.Hash(hashes.SHA512(), backend=default_backend())
        digest.update(data)
        return digest.finalize()

    def hashlen(self):
        return 64

    def hmac_hash(self, key, data):
        hmac = HMAC(key=key, algorithm=hashes.SHA512(), backend=default_backend())
        hmac.update(data=data)
        return hmac.finalize()
