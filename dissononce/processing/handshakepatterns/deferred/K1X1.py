from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class K1X1HandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(K1X1HandshakePattern, self).__init__(
            'K1X1',
            initiator_pre_messages=('s',),
            message_patterns=(
                ('e',),
                ('e', 'ee', 's'),
                ('se', 'es')
            )
        )
