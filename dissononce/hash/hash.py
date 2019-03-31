class Hash(object):
    def __init__(self, name, hashlen, blocklen):
        """
        :param name: Name of hash function algorithm
        :type name: str
        :param hashlen: HASHLEN = size in bytes of the hash output. Must be 32 or 64.
        :type hashlen: int
        :param blocklen: BLOCKLEN = size in bytes that the hash function uses internally to divide its input for
        iterative processing. This is needed to use the hash function with HMAC
        :type blocklen: int
        """
        assert hashlen in (32, 64), "Unsupported hashlen %d" % hashlen
        self._name = name  # type: str
        self._hashlen = hashlen  # type: int
        self._blocklen = blocklen  # type: int

    @property
    def name(self):
        return self._name

    @property
    def hashlen(self):
        return self._hashlen

    @property
    def blocklen(self):
        return self._blocklen

    def hash(self, data):
        """
        Hashes some arbitrary-length data with a collision-resistant cryptographic
        hash function and returns an output of HASHLEN bytes.
        :param data:
        :type data: bytes
        :return:
        :rtype: bytes
        """

    def hmac_hash(self, key, data):
        """
        HMAC-HASH(key, data)
        Applies HMAC using the HASH() function. This function is only called as part of HKDF()
        :param key:
        :type key: bytes
        :param data:
        :type data: bytes
        :return:
        :rtype: bytes
        """
        pass

    def hkdf(self, chaining_key, input_key_material, num_outputs):
        """
        HKDF(chaining_key, input_key_material, num_outputs)
        Takes a chaining_key byte sequence of length HASHLEN, and an input_key_material byte sequence with length
        either zero bytes, 32 bytes, or DHLEN bytes.
        Returns a pair or triple of byte sequences each of length HASHLEN, depending on whether num_outputs is
        two or three

        Sets temp_key = HMAC-HASH(chaining_key, input_key_material).
        Sets output1 = HMAC-HASH(temp_key, byte(0x01)).
        Sets output2 = HMAC-HASH(temp_key, output1 || byte(0x02)).
        If num_outputs == 2 then returns the pair (output1, output2).
        Sets output3 = HMAC-HASH(temp_key, output2 || byte(0x03)).
        Returns the triple (output1, output2, output3).

        :param chaining_key:
        :type chaining_key: bytes
        :param input_key_material:
        :type input_key_material: bytes
        :param num_outputs:
        :type num_outputs: int
        :return:
        :rtype: tuple
        """
        temp_key = self.hmac_hash(chaining_key, input_key_material)

        # Sets output1 = HMAC-HASH(temp_key, byte(0x01)).
        output1 = self.hmac_hash(temp_key, b'\x01')

        # Sets output2 = HMAC-HASH(temp_key, output1 || byte(0x02)).
        output2 = self.hmac_hash(temp_key, output1 + b'\x02')

        # If num_outputs == 2 then returns the pair (output1, output2).
        if num_outputs == 2:
            return output1, output2

        # Sets output3 = HMAC-HASH(temp_key, output2 || byte(0x03)).
        output3 = self.hmac_hash(temp_key, output2 + b'\x03')

        # Returns the triple (output1, output2, output3).
        return output1, output2, output3
