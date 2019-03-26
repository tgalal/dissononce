from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class K1K1HandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(K1K1HandshakePattern, self).__init__(
            'K1K1',
            initiator_pre_messages=('s',),
            responder_pre_message_pattern=('s',),
            message_patterns=(
                ('e',),
                ('e', 'ee', 'es'),
                ('se',)
            )
        )
