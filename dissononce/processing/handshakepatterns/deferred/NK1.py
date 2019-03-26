from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class NK1HandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(NK1HandshakePattern, self).__init__(
            'NK1',
            responder_pre_message_pattern=('s',),
            message_patterns=(
                ('e',),
                ('e', 'ee', 'es')
            )
        )
