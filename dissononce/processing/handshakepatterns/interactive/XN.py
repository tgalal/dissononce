from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class XNHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(XNHandshakePattern, self).__init__(
            'XN',
            message_patterns=(
                ('e',),
                ('e', 'ee'),
                ('s', 'se')
            )
        )
