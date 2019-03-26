from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class KNHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(KNHandshakePattern, self).__init__(
            'KN',
            initiator_pre_messages=('s',),
            message_patterns=(
                ('e',),
                ('e', 'ee', 'se')
            )
        )
