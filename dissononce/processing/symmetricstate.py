class SymmetricState(object):
    @property
    def ciphername(self):
        return None

    @property
    def hashname(self):
        return None

    def ciherstate_has_key(self):
        pass

    def initialize_symmetric(self, protocolname):
        """
        :param protocolname:
        :type protocolname: bytes
        :return:
        :rtype:
        """

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

    def mix_hash(self, data):
        """
        MixHash(data):
        Sets h = HASH(h || data).

        :param data:
        :type data: bytes
        :return:
        :rtype:
        """

    def mix_key_and_hash(self, input_key_material):
        """
        :param input_key_material:
        :type input_key_material: bytes
        :return:
        :rtype:
        """

    def get_handshake_hash(self):
        """
        GetHandshakeHash():
        Returns h. This function should only be called at the end of a handshake,
        i.e. after the Split() function has been called

        :return: h
        :rtype: bytes
        """

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
