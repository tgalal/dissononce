class DecryptFailedException(Exception):
    REASON_INVALID_TAG = 0

    def __init__(self, reason):
        super(DecryptFailedException, self).__init__()
        self._reason = reason

    @property
    def reason(self):
        return self._reason
