from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class NXHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(NXHandshakePattern, self).__init__(
            'NX',
            message_patterns=(
                ('e',),
                ('e', 'ee', 's', 'es')
            )
        )
