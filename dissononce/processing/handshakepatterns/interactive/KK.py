from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class KKHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(KKHandshakePattern, self).__init__(
            'KK',
            initiator_pre_messages=('s',),
            responder_pre_message_pattern=('s',),
            message_patterns=(
                ('e', 'es', 'ss'),
                ('e', 'ee', 'se')
            )
        )
