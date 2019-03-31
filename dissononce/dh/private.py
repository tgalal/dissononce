class PrivateKey(object):

    def __init__(self, data):
        """
        :param data: bytes
        """
        self._data = data

    @property
    def data(self):
        """
        :return: bytes
        """
        return self._data
