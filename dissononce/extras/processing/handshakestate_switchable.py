from dissononce.extras.processing.handshakestate_forwarder import ForwarderHandshakeState


class SwitchableHandshakeState(ForwarderHandshakeState):
    """SwitchableHandshakeState facilitates transforming an ongoing Handshake into using a different pattern.
    Given the newHandshakePattern, it analyses the required initiator and responder pre-messages, and maintains them
    across the transformation for use in the new Handshake. This is typically used for example when doing a IK
    handshake then switching to XXfallback where re is to be used as a initiator pre-message."""
    def __init__(self, handshakestate):
        """
        :param handshakestate:
        :type handshakestate: HandshakeState
        """
        super(SwitchableHandshakeState, self).__init__(handshakestate)

    def switch(self, handshake_pattern, initiator, prologue, s=None, e=None, rs=None, re=None, psks=None):
        if initiator:
            for pattern in handshake_pattern.initiator_pre_message_pattern:
                for token in pattern:
                    if token == 'e':
                        e = self.e
                    if token == 's':
                        s = self.s

            for pattern in handshake_pattern.responder_pre_message_pattern:
                for token in pattern:
                    if token == 'e':
                        re = self.re
                    if token == 's':
                        rs = self.rs
        else:
            for pattern in handshake_pattern.initiator_pre_message_pattern:
                for token in pattern:
                    if token == 'e':
                        re = self.re
                    if token == 's':
                        rs = self.rs

            for pattern in handshake_pattern.responder_pre_message_pattern:
                for token in pattern:
                    if token == 'e':
                        e = self.e
                    if token == 's':
                        s = self.s

        return self.initialize(handshake_pattern, initiator, prologue, s, e, rs, re, psks)
