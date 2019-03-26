from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class K1NHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(K1NHandshakePattern, self).__init__(
            'K1N',
            initiator_pre_messages=('s',),
            message_patterns=(
                ('e',),
                ('e', 'ee'),
                ('se',)
            )
        )
