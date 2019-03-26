from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class K1XHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(K1XHandshakePattern, self).__init__(
            'K1X',
            initiator_pre_messages=('s',),
            message_patterns=(
                ('e',),
                ('e', 'ee', 's', 'es'),
                ('se',)
            )
        )
