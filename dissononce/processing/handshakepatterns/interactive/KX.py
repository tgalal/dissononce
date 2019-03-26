from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class KXHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(KXHandshakePattern, self).__init__(
            'KX',
            initiator_pre_messages=('s',),
            message_patterns=(
                ('e',),
                ('e', 'ee', 'se', 's', 'es')
            )
        )
