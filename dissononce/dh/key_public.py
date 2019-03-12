class PublicKey(object):

    def __init__(self, data):
        """
        :param data: bytes
        """
        if len(data) != 32:
            raise ValueError("Wrong length: %d" % len(data))

        self._data = data

    @property
    def data(self):
        """
        :return: bytes
        """
        return self._data
