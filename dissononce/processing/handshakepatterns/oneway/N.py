from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class NHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(NHandshakePattern, self).__init__(
            'N',
            responder_pre_message_pattern=('s',),
            message_patterns=(
                ('e', 'es'),
            )
        )
