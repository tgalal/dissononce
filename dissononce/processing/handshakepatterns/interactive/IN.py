from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class INHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(INHandshakePattern, self).__init__(
            'IN',
            message_patterns=(
                ('e', 's'),
                ('e', 'ee', 'se')
            )
        )
