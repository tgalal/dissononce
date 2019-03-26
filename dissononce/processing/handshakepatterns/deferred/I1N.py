from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class I1NHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(I1NHandshakePattern, self).__init__(
            'I1N',
            message_patterns=(
                ('e', 's'),
                ('e', 'ee'),
                ('se',)
            )
        )
