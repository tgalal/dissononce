from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class IKHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(IKHandshakePattern, self).__init__(
            'IK',
            responder_pre_message_pattern=('s',),
            message_patterns=(
                ('e', 'es', 's', 'ss'),
                ('e', 'ee', 'se')
            )
        )
