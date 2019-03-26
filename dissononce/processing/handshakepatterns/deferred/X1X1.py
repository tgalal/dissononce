from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class X1X1HandshakePattern(HandshakePattern):
    def __init__(self):
        super(X1X1HandshakePattern, self).__init__(
            'X1X1',
            message_patterns=(
                ('e',),
                ('e', 'ee', 's'),
                ('es', 's'),
                ('se',)
            )
        )
