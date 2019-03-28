class PublicKey(object):

    def __init__(self, keylen, data):
        """
        :param data: bytes
        """
        if len(data) != keylen:
           raise ValueError("Wrong length: %d" % len(data))

        self._data = data

    @property
    def data(self):
        """
        :return: bytes
        """
        return self._data
