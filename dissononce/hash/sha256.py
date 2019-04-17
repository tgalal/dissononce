from dissononce.hash.hash import Hash

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hmac import HMAC


class SHA256Hash(Hash):
    def __init__(self):
        super(SHA256Hash, self).__init__("SHA256", 32, 64)

    def hash(self, data):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(data)
        return digest.finalize()

    def hmac_hash(self, key, data):
        hmac = HMAC(key=key, algorithm=hashes.SHA256(), backend=default_backend())
        hmac.update(data=data)
        return hmac.finalize()
