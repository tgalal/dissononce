from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class IXHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(IXHandshakePattern, self).__init__(
            'IX',
            message_patterns=(
                ('e', 's'),
                ('e', 'ee', 'se', 's', 'es')
            )
        )
