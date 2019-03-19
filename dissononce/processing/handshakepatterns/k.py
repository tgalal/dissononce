from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class KHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(KHandshakePattern, self).__init__(
            "K",
            message_patterns=(
                ("e", "es", "ss"),
            ),
            initiator_pre_messages=("s",),
            responder_pre_message_pattern=("s",),
        )
