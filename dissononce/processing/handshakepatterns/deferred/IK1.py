from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class IK1HandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(IK1HandshakePattern, self).__init__(
            'IK1',
            responder_pre_message_pattern= ('s',),
            message_patterns=(
                ('e', 's'),
                ('e', 'ee', 'se', 'es')
            )
        )
