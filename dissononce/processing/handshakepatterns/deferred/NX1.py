from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class NX1HandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(NX1HandshakePattern, self).__init__(
            'NX1',
            message_patterns=(
                ('e',),
                ('e', 'ee', 's'),
                ('es',)
            )
        )
