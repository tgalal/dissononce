from dissononce.processing.impl.cipherstate import CipherState
from dissononce.processing.symmetricstate import SymmetricState as BaseSymmetricState
from dissononce.hash.hash import Hash


class SymmetricState(BaseSymmetricState):
    def __init__(self, cipherstate, hash):
        """
        :param cipherstate:
        :type cipherstate: CipherState
        :param hash:
        :type hash: Hash
        """
        self._cipherstate = cipherstate
        self._hashfn = hash
        self._ck =  None
        self._h = None

    @property
    def ciphername(self):
        return self._cipherstate.cipher.name

    @property
    def hashname(self):
        return self._hashfn.name

    def ciherstate_has_key(self):
        return self._cipherstate.has_key()

    def initialize_symmetric(self, protocolname):
        """
        :param protocolname:
        :type protocolname: bytes
        :return:
        :rtype:
        """
        lendiff = len(protocolname) - self._hashfn.hashlen()

        if lendiff <= 0:
            self._h = protocolname + b"\0" * abs(lendiff)
        else:
            self._h = self._hashfn.hash(protocolname)

        self._ck = self._h

    def mix_key(self, input_key_material):
        """
        MixKey(input_key_material):
        Executes the following steps:
        Sets ck, temp_k = HKDF(ck, input_key_material, 2).
        If HASHLEN is 64, then truncates temp_k to 32 bytes.
        Calls InitializeKey(temp_k).

        :param input_key_material:
        :type input_key_material: bytes
        :return:
        :rtype:
        """
        self._ck, temp_k = self._hashfn.hkdf(self._ck, input_key_material, 2)
        if self._hashfn.hashlen() == 64:
            temp_k = temp_k[:32]

        self._cipherstate.initialize_key(temp_k)

    def mix_hash(self, data):
        """
        MixHash(data):
        Sets h = HASH(h || data).

        :param data:
        :type data: bytes
        :return:
        :rtype:
        """
        self._h = self._hashfn.hash(self._h + data)

    def mix_key_and_hash(self, input_key_material):
        """
        This function is used for handling pre-shared symmetric keys. It executes the following steps:

        Sets ck, temp_h, temp_k = HKDF(ck, input_key_material, 3).
        Calls MixHash(temp_h).
        If HASHLEN is 64, then truncates temp_k to 32 bytes.
        Calls InitializeKey(temp_k).

        :param input_key_material:
        :type input_key_material: bytes
        :return:
        :rtype:
        """
        self._ck, temp_h, temp_k = self._hashfn.hkdf(self._ck, input_key_material, 3)
        self.mix_hash(temp_h)
        if self._hashfn.hashlen() == 64:
            temp_k = temp_k[:32]
        self._cipherstate.initialize_key(temp_k)

    def get_handshake_hash(self):
        """
        GetHandshakeHash():
        Returns h. This function should only be called at the end of a handshake,
        i.e. after the Split() function has been called

        :return: h
        :rtype: bytes
        """
        return self._h

    def encrypt_and_hash(self, plaintext):
        """
        EncryptAndHash(plaintext):
        Sets ciphertext = EncryptWithAd(h, plaintext), calls MixHash(ciphertext), and returns ciphertext.
        Note that if k is empty, the EncryptWithAd() call will set ciphertext equal to plaintext

        :param plaintext:
        :type plaintext: bytes
        :return:
        :rtype: bytes
        """
        ciphertext = self._cipherstate.encrypt_with_ad(self._h, plaintext)
        self.mix_hash(ciphertext)
        return ciphertext

    def decrypt_and_hash(self, ciphertext):
        """
        DecryptAndHash(ciphertext):
        Sets plaintext = DecryptWithAd(h, ciphertext), calls MixHash(ciphertext), and returns plaintext.
        Note that if k is empty, the DecryptWithAd() call will set plaintext equal to ciphertext.

        :param ciphertext:
        :type ciphertext: bytes
        :return:
        :rtype: bytes
        """
        plaintext = self._cipherstate.decrypt_with_ad(self._h, ciphertext)
        self.mix_hash(ciphertext)
        return plaintext

    def split(self):
        """
        Split():
        Returns a pair of CipherState objects for encrypting transport messages.
        Executes the following steps, where zerolen is a zero-length byte sequence:

        Sets temp_k1, temp_k2 = HKDF(ck, zerolen, 2).
        If HASHLEN is 64, then truncates temp_k1 and temp_k2 to 32 bytes.
        Creates two new CipherState objects c1 and c2.
        Calls c1.InitializeKey(temp_k1) and c2.InitializeKey(temp_k2).
        Returns the pair (c1, c2).

        :return:
        :rtype: tuple
        """
        temp_k1, temp_k2 = self._hashfn.hkdf(self._ck, b"", 2)
        if self._hashfn.hashlen() == 64:
            temp_k1 = temp_k1[:32]
            temp_k2 = temp_k2[:32]

        c1 = CipherState(self._cipherstate.cipher)
        c2 = CipherState(self._cipherstate.cipher)
        c1.initialize_key(temp_k1)
        c2.initialize_key(temp_k2)

        return c1, c2
