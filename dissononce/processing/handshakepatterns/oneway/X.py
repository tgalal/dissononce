from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class XHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(XHandshakePattern, self).__init__(
            'X',
            responder_pre_message_pattern=('s',),
            message_patterns=(
                ('e', 'es', 's', 'ss'),
            )
        )
