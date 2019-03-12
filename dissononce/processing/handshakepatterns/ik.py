from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class IKHandshakePattern(HandshakePattern):
    def __init__(self, ):
        super(IKHandshakePattern, self).__init__(
            "IK",
            message_patterns=(
                ("e", "es", "s", "ss"),
                ("e", "ee", "se")
            ),
            initiator_pre_messages= ("s",),
        )
