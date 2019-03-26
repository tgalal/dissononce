from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class I1X1HandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(I1X1HandshakePattern, self).__init__(
            'I1X1',
            message_patterns=(
                ('e', 's'),
                ('e', 'ee', 's'),
                ('se', 'es')
            )
        )
