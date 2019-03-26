from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class XXHandshakePattern(HandshakePattern):
    def __init__(self):
        super(XXHandshakePattern, self).__init__(
            'XX',
            message_patterns=(
                ('e',),
                ('e', 'ee', 's', 'es'),
                ('s', 'se')
            )
        )
