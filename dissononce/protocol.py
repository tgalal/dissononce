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
        self._cipherstate = CipherState(cipher)  # type: CipherState
        self._symmetricstate = SymmetricState(self._cipherstate, self._hash)  # type: SymmetricState
        self._handshakestate = HandshakeState(self._symmetricstate, dh or self._dh)  # type: HandshakeState
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

    @property
    def cipherstate(self):
        return self._cipherstate

    @property
    def symmetricstate(self):
        return self._symmetricstate

    @property
    def handshakestate(self):
        return self._handshakestate
