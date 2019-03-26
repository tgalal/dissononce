from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class X1NHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(X1NHandshakePattern, self).__init__(
            'X1N',
            message_patterns=(
                ('e',),
                ('e', 'ee'),
                ('s', ),
                ('se',)
            )
        )
