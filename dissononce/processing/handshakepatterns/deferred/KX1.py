from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class KX1HandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(KX1HandshakePattern, self).__init__(
            'KX1',
            initiator_pre_messages=('s',),
            message_patterns=(
                ('e',),
                ('e', 'ee', 'se', 's'),
                ('es',)
            )
        )
