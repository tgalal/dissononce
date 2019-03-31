from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class X1K1HandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(X1K1HandshakePattern, self).__init__(
            'X1K1',
            responder_pre_message_pattern=('s',),
            message_patterns=(
                ('e',),
                ('e', 'ee', 'es'),
                ('s',),
                ('se',)
            )
        )
