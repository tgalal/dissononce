from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class KK1HandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(KK1HandshakePattern, self).__init__(
            'KK1',
            initiator_pre_messages=('s',),
            responder_pre_message_pattern=('s',),
            message_patterns=(
                ('e',),
                ('e', 'ee', 'se', 'es')
            )
        )
