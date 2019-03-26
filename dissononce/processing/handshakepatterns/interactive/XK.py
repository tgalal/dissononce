from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class XKHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(XKHandshakePattern, self).__init__(
            'XK',
            responder_pre_message_pattern= ('s',),
            message_patterns=(
                ('e', 'es'),
                ('e', 'ee'),
                ('s', 'se')
            )
        )
