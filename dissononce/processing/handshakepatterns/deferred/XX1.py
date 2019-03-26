from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class XX1HandshakePattern(HandshakePattern):
    def __init__(self):
        super(XX1HandshakePattern, self).__init__(
            'XX1',
            message_patterns=(
                ('e',),
                ('e', 'ee', 's'),
                ('es', 's', 'se')
            )
        )
