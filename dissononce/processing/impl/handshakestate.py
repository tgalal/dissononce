from dissononce.processing.symmetricstate import SymmetricState
from dissononce.processing.handshakestate import HandshakeState as BaseHandshakeState

from dissononce.dh.public import PublicKey
from dissononce.dh.keypair import KeyPair
from dissononce.dh.dh import DH

import logging

logger = logging.getLogger(__name__)


class HandshakeState(BaseHandshakeState):
    _TEMPLATE_PROTOCOL_NAME = "Noise_{handshake}_{dh}_{cipher}_{hash}"

    def __init__(self, symmetricstate, dh):
        """
        :param symmetricstate:
        :type symmetricstate: SymmetricState
        :param dh
        :type DH
        """
        self._symmetricstate = symmetricstate  # type: SymmetricState
        self._dh = dh  # type: DH
        self._s = None  # type: KeyPair
        self._e = None  # type: KeyPair | None
        self._rs = None  # type: PublicKey | None
        self._re = None  # type: PublicKey | None
        self._initiator = None
        self._message_patterns = None  # type: list[tuple[str]]
        self._protocol_name = None  # type: str | None

    @property
    def protocol_name(self):
        return self._protocol_name

    @property
    def symmetricstate(self):
        return self._symmetricstate

    @property
    def rs(self):
        return self._rs

    @property
    def re(self):
        return self._re

    @property
    def s(self):
        return self._s

    @property
    def e(self):
        return self._e

    def initialize(self, handshake_pattern, initiator, prologue, s=None, e=None, rs=None, re=None, psks=None):
        self._protocol_name = self._derive_protocol_name(handshake_pattern.name)
        self._symmetricstate.initialize_symmetric(self._protocol_name.encode())
        self._symmetricstate.mix_hash(prologue)
        self._initiator = initiator
        self._s = s
        self._e = e
        self._rs = rs
        self._re = re

        self._psks = list(psks) if psks is not None else psks
        self._pskmode = 'psk' in handshake_pattern.name

        logger.info("Derived Noise Protocol name %s" % self._protocol_name)
        logger.debug("\n%s", handshake_pattern)

        if len(handshake_pattern.initiator_pre_message_pattern) or len(handshake_pattern.responder_pre_message_pattern):
            logger.info("Processing pre-messages")

            if initiator:
                for token in handshake_pattern.initiator_pre_message_pattern:
                    if token == 's':
                        logger.debug("MixHash(s.public_key)")
                        self._symmetricstate.mix_hash(s.public.data)
                    if token == 'e':
                        logger.debug("MixHash(e.public_key)")
                        self._symmetricstate.mix_hash(e.public.data)
                        if self._pskmode:
                            self._symmetricstate.mix_key(e.public.data)

                for token in handshake_pattern.responder_pre_message_pattern:
                    if token == 's':
                        logger.debug("MixHash(rs)")
                        assert rs is not None, "a pre_message required rs but was empty"
                        self._symmetricstate.mix_hash(rs.data)
                    elif token == 'e':
                        logger.debug("MixHash(re)")
                        assert re is not None, "a pre_message required re but was empty"
                        self._symmetricstate.mix_hash(re.data)

            else:
                for token in handshake_pattern.initiator_pre_message_pattern:
                    if token == 's':
                        logger.debug("MixHash(rs)")
                        assert rs is not None, "a pre_message required rs but was empty"
                        self._symmetricstate.mix_hash(rs.data)
                    elif token == 'e':
                        logger.debug("MixHash(re)")
                        assert re is not None, "a pre_message required re but was empty"
                        self._symmetricstate.mix_hash(re.data)

                for token in handshake_pattern.responder_pre_message_pattern:
                    if token == 's':
                        logger.debug("MixHash(s.public_key)")
                        self._symmetricstate.mix_hash(s.public.data)
                    elif token == 'e':
                        logger.debug("MixHash(e.public_key)")
                        self._symmetricstate.mix_hash(e.public.data)
                        if self._pskmode:
                            self._symmetricstate.mix_key(e.public.data)

        self._message_patterns = list(handshake_pattern.message_patterns)

    def _derive_protocol_name(self, handshake_pattern_name):
        return self.__class__._TEMPLATE_PROTOCOL_NAME.format(
            handshake=handshake_pattern_name,
            dh=self._dh.name,
            cipher=self._symmetricstate.ciphername,
            hash=self._symmetricstate.hashname
        )

    def write_message(self, payload, message_buffer):
        """
        :param payload:
        :type payload: bytes
        :param message_buffer:
        :type message_buffer: bytearray
        :return:
        :rtype: tuple | None
        """
        logger.info("WriteMessage(payload, message_buffer)")
        message_pattern = self._message_patterns.pop(0)

        for token in message_pattern:
            logger.debug("    Processing token '%s'" % token)
            if token == 'e':
                assert self._e is None, "e is not empty"

                logger.debug("        e=GENERATE_KEYPAIR()")
                self._e = self._dh.generate_keypair()

                logger.debug("        message_buffer.append(e.public_key)")
                message_buffer.extend(self._e.public.data)

                logger.debug("        MixHash(e.public_key)")
                self._symmetricstate.mix_hash(self._e.public.data)
                if self._pskmode:
                    logger.debug("        MixKey(e.public_key)")
                    self._symmetricstate.mix_key(self._e.public.data)
            elif token == 's':
                assert self._s is not None, "s is empty"
                logger.debug("        buffer.append(EncryptAndHash(s.public_key))")
                message_buffer.extend(self._symmetricstate.encrypt_and_hash(self._s.public.data))
            elif token == 'ee':
                logger.debug("        MixKey(DH(e, re))")
                self._symmetricstate.mix_key(self._dh.dh(self._e, self._re))
            elif token == 'es':
                if self._initiator:
                    logger.debug("        MixKey(DH(e, rs))")
                    self._symmetricstate.mix_key(self._dh.dh(self._e, self._rs))
                else:
                    logger.debug("        MixKey(DH(s, re))")
                    self._symmetricstate.mix_key(self._dh.dh(self._s, self._re))
            elif token == 'se':
                if self._initiator:
                    logger.debug("        MixKey(DH(s, re))")
                    self._symmetricstate.mix_key(self._dh.dh(self._s, self._re))
                else:
                    logger.debug("        MixKey(DH(e, rs))")
                    self._symmetricstate.mix_key(self._dh.dh(self._e, self._rs))
            elif token == 'ss':
                logger.debug("        MixKey(DH(s, rs))")
                self._symmetricstate.mix_key(self._dh.dh(self._s, self._rs))
            elif token == 'psk':
                assert self._psks is not None and len(self._psks), "psks is empty"
                self._symmetricstate.mix_key_and_hash(self._psks.pop(0))
            else:
                raise ValueError("Unsupported token '%s' found in message_pattern" % token)

        logger.debug("    buffer.append(EncryptAndHash(payload))")
        message_buffer.extend(self._symmetricstate.encrypt_and_hash(payload))

        if len(self._message_patterns) == 0:
            return self._symmetricstate.split()

    def read_message(self, message, payload_buffer):
        """
        :param message:
        :type message: bytes
        :param payload_buffer:
        :type payload_buffer: bytearray
        :return:
        :rtype: tuple | None
        """
        logger.info("ReadMessage(message, payload_buffer)")
        message_pattern = self._message_patterns.pop(0)

        for token in message_pattern:
            logger.debug("    Processing token '%s'" % token)
            if token == 'e':
                assert self._re is None, "re is not empty"
                logger.debug("        re=message[:DHLEN]")
                self._re = self._dh.create_public(message[:self._dh.dhlen])
                logger.debug("        MixHash(re.public_key)")
                self._symmetricstate.mix_hash(self._re.data)
                message = message[self._dh.dhlen:]

                if self._pskmode:
                    logger.debug("        MixKey(re.public_key)")
                    self._symmetricstate.mix_key(self._re.data)
            elif token == 's':
                if self._symmetricstate.ciherstate_has_key():
                    logger.debug("        temp=message[:DHLEN + 16]")
                    temp = message[:self._dh.dhlen + 16]
                else:
                    logger.debug("        temp=message[:DHLEN]")
                    temp = message[:self._dh.dhlen]
                assert self._rs is None, "rs is not empty"
                logger.debug("        rs=DecryptAndHash(temp)")
                self._rs = self._dh.create_public(self._symmetricstate.decrypt_and_hash(temp))
                message = message[len(temp):]
            elif token == 'ee':
                logger.debug("        MixKey(DH(e, re))")
                self._symmetricstate.mix_key(self._dh.dh(self._e, self._re))
            elif token == 'es':
                if self._initiator:
                    logger.debug("        MixKey(DH(e, rs))")
                    self._symmetricstate.mix_key(self._dh.dh(self._e, self._rs))
                else:
                    logger.debug("        MixKey(DH(s, re))")
                    self._symmetricstate.mix_key(self._dh.dh(self._s, self._re))
            elif token == 'se':
                if self._initiator:
                    logger.debug("        MixKey(DH(s, re))")
                    self._symmetricstate.mix_key(self._dh.dh(self._s, self._re))
                else:
                    logger.debug("        MixKey(DH(e, rs))")
                    self._symmetricstate.mix_key(self._dh.dh(self._e, self._rs))
            elif token == 'ss':
                logger.debug("        MixKey(DH(s, rs))")
                self._symmetricstate.mix_key(self._dh.dh(self._s, self._rs))
            elif token == 'psk':
                assert self._psks is not None and len(self._psks), "psks is empty"
                self._symmetricstate.mix_key_and_hash(self._psks.pop(0))
            else:
                raise ValueError("Unsupported token '%s' found in message_pattern" % token)

        logger.debug("    DecryptAndHash(message[remaining:])")
        payload_buffer.extend(self._symmetricstate.decrypt_and_hash(message))

        if len(self._message_patterns) == 0:
            return self._symmetricstate.split()
