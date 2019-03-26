from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class I1XHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(I1XHandshakePattern, self).__init__(
            'I1X',
            message_patterns=(
                ('e', 's'),
                ('e', 'ee', 's', 'es'),
                ('se',)
            )
        )
