from dissononce.cipher.cipher import Cipher

import struct
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


class ChaChaPolyCipher(Cipher):
    def __init__(self):
        super(ChaChaPolyCipher, self).__init__("ChaChaPoly")

    def encrypt(self, key, nonce, ad, plaintext):
        return ChaCha20Poly1305(key).encrypt(self.__class__._format_nonce(nonce), plaintext, ad)

    def decrypt(self, key, nonce, ad, ciphertext):
        return ChaCha20Poly1305(key).decrypt(self.__class__._format_nonce(nonce), ciphertext, ad)

    @staticmethod
    def _format_nonce(n):
        return b'\x00\x00\x00\x00' + struct.pack('<Q', n)
