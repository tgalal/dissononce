from dissononce.processing.handshakestate import HandshakeState


class ForwarderHandshakeState(HandshakeState):
    def __init__(self, handshakestate):
        """
        :param handshakestate:
        :type handshakestate: HandshakeState
        """
        self._handshakestate = handshakestate

    def initialize(self, handshake_pattern, initiator, prologue, s=None, e=None, rs=None, re=None):
        return self._handshakestate.initialize(handshake_pattern, initiator, prologue, s, e, rs, re)

    def write_message(self, payload, message_buffer):
        return self._handshakestate.write_message(payload, message_buffer)

    def read_message(self, message, payload_buffer):
        return self._handshakestate.read_message(message, payload_buffer)

    @property
    def re(self):
        return self._handshakestate.re

    @property
    def rs(self):
        return self._handshakestate.rs

    @property
    def s(self):
        return self._handshakestate.s

    @property
    def e(self):
        return self._handshakestate.e
