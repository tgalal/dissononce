class Hash(object):
    def __init__(self, name, hashlen, blocklen):
        """
        :param name:
        :type name: str
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
        '''
        :param data:
        :type data: bytes
        :return:
        :rtype: bytes

    def hmac_hash(self, key, data):
        pass


    def hkdf(self, chaining_key, input_key_material, num_outputs):
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


