from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class K1KHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(K1KHandshakePattern, self).__init__(
            'K1K',
            initiator_pre_messages=('s',),
            responder_pre_message_pattern=('s',),
            message_patterns=(
                ('e', 'es'),
                ('e', 'ee'),
                ('se',)
            )
        )
