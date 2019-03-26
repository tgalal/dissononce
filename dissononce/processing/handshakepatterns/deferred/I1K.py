from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class I1KHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(I1KHandshakePattern, self).__init__(
            'I1K',
            responder_pre_message_pattern= ('s',),
            message_patterns=(
                ('e', 'es', 's'),
                ('e', 'ee'),
                ('se',)
            )
        )
