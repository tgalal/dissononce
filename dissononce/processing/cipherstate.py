from dissononce.cipher.cipher import Cipher


class CipherState(object):
    def __init__(self, cipher):
        """
        :param cipher:
        :type cipher: Cipher
        """
        self._cipher = cipher
        self._key = None
        self._nonce = 0
    
    @property
    def cipher(self):
        return self._cipher

    def initialize_key(self, key):
        self._key = key
        self.set_nonce(0)

    def has_key(self):
        return self._key is not None

    def set_nonce(self, nonce):
        """
        SetNonce(nonce): Sets n = nonce.
        This function is used for handling out-of-order transport messages

        :param nonce:
        :type nonce: int
        :return:
        :rtype:
        """
        self._nonce = nonce

    def rekey(self):
        self.initialize_key(self._cipher.rekey(self._key))

    def encrypt_with_ad(self, ad, plaintext):
        """
        EncryptWithAd(ad, plaintext):
        If k is non-empty returns ENCRYPT(k, n++, ad, plaintext). Otherwise returns plaintext.

        :param ad:
        :type ad: bytes
        :param plaintext:
        :type plaintext: bytes
        :return:
        :rtype: bytes
        """
        if self._key is None:
            return plaintext

        result = self._cipher.encrypt(self._key, self._nonce, ad, plaintext)
        self._nonce += 1
        return result

    def decrypt_with_ad(self, ad, ciphertext):
        """
        DecryptWithAd(ad, ciphertext):
        If k is non-empty returns DECRYPT(k, n++, ad, ciphertext). Otherwise returns ciphertext.
        If an authentication failure occurs in DECRYPT() then n is not incremented
        and an error is signaled to the caller.

        :param ad:
        :type ad: bytes
        :param ciphertext:
        :type ciphertext: bytes
        :return: bytes
        :rtype:
        """
        if self._key is None:
            return ciphertext

        result = self._cipher.decrypt(self._key, self._nonce, ad, ciphertext)
        self._nonce += 1
        return result
