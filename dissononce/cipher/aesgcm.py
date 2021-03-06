from dissononce.cipher.cipher import Cipher
from dissononce.exceptions.decrypt import DecryptFailedException

import struct
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag


class AESGCMCipher(Cipher):
    def __init__(self):
        super(AESGCMCipher, self).__init__("AESGCM")

    def encrypt(self, key, nonce, ad, plaintext):
        return AESGCM(key).encrypt(self.__class__._format_nonce(nonce), plaintext, ad)

    def decrypt(self, key, nonce, ad, ciphertext):
        try:
            return AESGCM(key).decrypt(self.__class__._format_nonce(nonce), ciphertext, ad)
        except InvalidTag:
            raise DecryptFailedException(reason=DecryptFailedException.REASON_INVALID_TAG)

    @staticmethod
    def _format_nonce(n):
        return b'\x00\x00\x00\x00' + struct.pack('>Q', n)
