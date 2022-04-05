class VectorMessage(object):
    def __init__(self, payload, ciphertext, from_initiator=None):
        self._payload = payload
        self._ciphertext = ciphertext
        self._from_initiator=from_initiator

    @property
    def payload(self):
        return self._payload

    @property
    def ciphertext(self):
        return self._ciphertext

    @property
    def from_initiator(self):
        return self._from_initiator
