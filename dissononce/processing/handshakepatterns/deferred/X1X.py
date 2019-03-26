from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class X1XHandshakePattern(HandshakePattern):
    def __init__(self):
        super(X1XHandshakePattern, self).__init__(
            'X1X',
            message_patterns=(
                ('e',),
                ('e', 'ee', 's', 'es'),
                ('s',),
                ('se',)
            )
        )
