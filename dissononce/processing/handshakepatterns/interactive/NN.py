from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class NNHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(NNHandshakePattern, self).__init__(
            'NN',
            message_patterns=(
                ('e', ),
                ('e', 'ee')
            )
        )
