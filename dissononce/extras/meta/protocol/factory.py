from dissononce.extras.meta.modifier.factory import ModifierFactory
from dissononce.extras.meta.hash.factory import HashFactory
from dissononce.extras.meta.cipher.factory import CipherFactory
from dissononce.extras.meta.dh.factory import DHFactory
from dissononce.extras.meta.pattern.factory import PatternFactory
from dissononce.extras.meta.protocol.protocol import NoiseProtocol
from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class NoiseProtocolFactory(object):

    def __init__(self):
        self._dh_factory = DHFactory()
        self._cipher_factory = CipherFactory()
        self._hash_factory = HashFactory()
        self._modifier_factory = ModifierFactory()
        self._pattern_factory = PatternFactory()

    def get_noise_protocol(self, name):
        """
        :param name:
        :type name: str
        :return:
        :rtype: NoiseProtocol
        """
        _, handshake, dh, cipher, hash = name.split('_')
        handshake_patternname, modifiers = HandshakePattern.parse_handshakepattern(handshake)

        pattern = self._pattern_factory.get_pattern(handshake_patternname)

        for modifier in modifiers:
            pattern = self._modifier_factory.get_modifier(modifier).modify(pattern)

        return NoiseProtocol(
            pattern,
            self._dh_factory.get_dh(dh),
            self._cipher_factory.get_cipher(cipher),
            self._hash_factory.get_hash(hash)
        )
