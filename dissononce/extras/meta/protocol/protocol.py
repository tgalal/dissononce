from dissononce.dh.dh import DH
from dissononce.cipher.cipher import Cipher
from dissononce.hash.hash import Hash
from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern

from dissononce.processing.impl.handshakestate import HandshakeState
from dissononce.processing.impl.symmetricstate import SymmetricState
from dissononce.processing.impl.cipherstate import CipherState


class NoiseProtocol(object):
    def __init__(self, pattern, dh, cipher, hash):
        """
        :param pattern:
        :type pattern:
        :param dh:
        :type dh:
        :param cipher:
        :type cipher:
        :param hash:
        :type hash:
        """
        self._pattern = pattern  # type: HandshakePattern
        self._dh = dh  # type: DH
        self._cipher = cipher  # type: Cipher
        self._hash = hash  # type: Hash
        self._oneway = len(HandshakePattern.parse_handshakepattern(pattern.name)[0]) == 1  # type: bool

    @property
    def oneway(self):
        return self._oneway

    @property
    def pattern(self):
        return self._pattern

    @property
    def dh(self):
        return self._dh

    @property
    def cipher(self):
        return self._cipher

    @property
    def hash(self):
        return self._hash

    def create_cipherstate(self, cipher=None):
        """
        :param cipher:
        :type cipher: Cipher
        :return:
        :rtype: CipherState
        """
        return CipherState(cipher or self._cipher)

    def create_symmetricstate(self, cipherstate=None, hash=None):
        """
        :param cipherstate:
        :type cipherstate: CipherState
        :param hash:
        :type hash: Hash
        :return:
        :rtype: SymmetricState
        """
        return SymmetricState(cipherstate or self.create_cipherstate(), hash or self._hash)

    def create_handshakestate(self, symmetricstate=None, dh=None):
        """
        :param symmetricstate:
        :type symmetricstate: SymmetricState
        :param dh:
        :type dh: DH
        :return:
        :rtype: HandshakeState
        """
        return HandshakeState(symmetricstate or self.create_symmetricstate(), dh or self._dh)
