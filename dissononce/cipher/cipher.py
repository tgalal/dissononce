class Cipher(object):
    def __init__(self, name):
        """
        :param name:
        :type name: str
        """
        self._name = name  # type: str

    @property
    def name(self):
        return self._name

    def encrypt(self, key, nonce, ad, plaintext):
        '''
        :param key:
        :type key: bytes
        :param nonce:
        :type nonce: int
        :param ad:
        :type ad: bytes
        :param plaintext:
        :type plaintext: bytes
        :return:
        :rtype: bytes
        '''

    def decrypt(self, key, nonce, ad, ciphertext):
        '''

        :param key:
        :type key: bytes
        :param nonce:
        :type nonce: int
        :param ad:
        :type ad: bytes
        :param ciphertext:
        :type ciphertext: bytes
        :return:
        :rtype: bytes
        '''

    def rekey(self, key):
        '''
        :param key:
        :type key: bytes
        :return:
        :rtype: bytes
        '''
        return self.encrypt(key, 2**64 - 1, b"", bytes([0] * 32))
