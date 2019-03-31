from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class X1KHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(X1KHandshakePattern, self).__init__(
            'X1K',
            responder_pre_message_pattern=('s',),
            message_patterns=(
                ('e', 'es'),
                ('e', 'ee'),
                ('s',),
                ('se',)
            )
        )
