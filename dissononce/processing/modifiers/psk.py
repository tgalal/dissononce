from dissononce.processing.modifiers.patternmodifier import PatternModifier


class PSKPatternModifier(PatternModifier):
    TOKEN = "psk"

    def __init__(self, placement):
        """
        :param placement:
        :type placement: int
        """
        super(PSKPatternModifier, self).__init__("psk%d" % placement)
        self._placement_index = 0 if placement == 0 else placement - 1
        self._placement_start = placement == 0

    def _is_modifiable(self, handsakepattern):
        return self._placement_index < len(handsakepattern.message_patterns) and \
               self.TOKEN not in handsakepattern.message_patterns[self._placement_index]

    def _get_message_patterns(self, handshakepattern):
        pattern = []
        for i in range(0, len(handshakepattern.message_patterns)):
            if i == self._placement_index:
                if self._placement_start:
                    pattern.append((self.TOKEN,) + handshakepattern.message_patterns[i])
                else:
                    pattern.append(handshakepattern.message_patterns[i] + (self.TOKEN,))
            else:
                pattern.append(handshakepattern.message_patterns[i])

        return tuple(pattern)

    def _get_initiator_pre_messages(self, handshakepattern):
        return handshakepattern.initiator_pre_message_pattern

    def _get_responder_pre_messages(self, handshakepattern):
        return handshakepattern.responder_pre_message_pattern
