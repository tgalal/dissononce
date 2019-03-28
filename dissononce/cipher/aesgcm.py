from dissononce.cipher.cipher import Cipher

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class AESGCMCipher(Cipher):
    def __init__(self):
        super(AESGCMCipher, self).__init__("AESGCM")

    def encrypt(self, key, nonce, ad, plaintext):
        return AESGCM(key).encrypt(self.__class__._format_nonce(nonce), plaintext, ad)

    def decrypt(self, key, nonce, ad, ciphertext):
        return AESGCM(key).decrypt(self.__class__._format_nonce(nonce), ciphertext, ad)

    @staticmethod
    def _format_nonce(n):
        return b'\x00\x00\x00\x00' + n.to_bytes(length=8, byteorder='big')
