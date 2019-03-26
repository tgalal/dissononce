from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class I1K1HandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(I1K1HandshakePattern, self).__init__(
            'I1K1',
            responder_pre_message_pattern= ('s',),
            message_patterns=(
                ('e', 's'),
                ('e', 'ee', 'es'),
                ('se',)
            )
        )
