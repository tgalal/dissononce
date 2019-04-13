class VectorMessage(object):
    def __init__(self, payload, ciphertext):
        self._payload = payload
        self._ciphertext = ciphertext

    @property
    def payload(self):
        return self._payload

    @property
    def ciphertext(self):
        return self._ciphertext
