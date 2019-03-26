from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class NKHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(NKHandshakePattern, self).__init__(
            'NK',
            responder_pre_message_pattern=('s',),
            message_patterns=(
                ('e', 'es'),
                ('e', 'ee')
            )
        )
