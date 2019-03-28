from dissononce.cipher.aesgcm import AESGCMCipher
from dissononce.cipher.chachapoly import ChaChaPolyCipher


NAME_CIPHER_AESGCM = 'AESGCM'
NAME_CIPHER_CHACHAPOLY = 'ChaChaPoly'


MAP_CIPHER = {
    NAME_CIPHER_AESGCM: AESGCMCipher,
    NAME_CIPHER_CHACHAPOLY: ChaChaPolyCipher
}
