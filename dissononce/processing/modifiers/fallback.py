from dissononce.processing.modifiers.patternmodifier import PatternModifier


class FallbackPatternModifier(PatternModifier):

    VALID_FIRST_MESSAGES = (('e',), ('s',), ('e', 's'))

    def __init__(self):
        super(FallbackPatternModifier, self).__init__("fallback")

    def _is_modifiable(self, handsakepattern):
        return handsakepattern.message_patterns[0] in self.__class__.VALID_FIRST_MESSAGES

    def _get_message_patterns(self, handshakepattern):
        return handshakepattern.message_patterns[1:]

    def _get_initiator_pre_messages(self, handshakepattern):
        return handshakepattern.message_patterns[0]

    def _interpret_as_bob(self, handshakepattern):
        return True

