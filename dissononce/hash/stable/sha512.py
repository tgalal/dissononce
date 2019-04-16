from dissononce.hash.hash import Hash

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hmac import HMAC


class SHA512Hash(Hash):
    def __init__(self):
        super(SHA512Hash, self).__init__("SHA512", 64, 128)

    def hash(self, data):
        digest = hashes.Hash(hashes.SHA512(), backend=default_backend())
        digest.update(data)
        return digest.finalize()

    def hmac_hash(self, key, data):
        hmac = HMAC(key=key, algorithm=hashes.SHA512(), backend=default_backend())
        hmac.update(data=data)
        return hmac.finalize()
