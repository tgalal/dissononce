from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class XK1HandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(XK1HandshakePattern, self).__init__(
            'XK1',
            responder_pre_message_pattern=('s',),
            message_patterns=(
                ('e',),
                ('e', 'ee', 'es'),
                ('s', 'se')
            )
        )
