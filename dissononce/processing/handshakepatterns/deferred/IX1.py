from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class IX1HandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(IX1HandshakePattern, self).__init__(
            'IX1',
            message_patterns=(
                ('e', 's'),
                ('e', 'ee', 'se', 's'),
                ('es',)
            )
        )
