from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern


class PatternModifier(object):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def _is_modifiable(self, handsakepattern):
        """
        :param handsakepattern:
        :type handsakepattern: HandshakePattern
        :return:
        :rtype: bool
        """

    def _get_message_patterns(self, handshakepattern):
        """
        :param handshakepattern:
        :type handshakepattern: HandshakePattern
        :return:
        :rtype: tuple
        """

    def _get_initiator_pre_messages(self, handshakepattern):
        """
        :param handshakepattern:
        :type handshakepattern: HandshakePattern
        :return:
        :rtype: tuple
        """
    def _get_responder_pre_messages(self, handshakepattern):
        """
        :param handshakepattern:
        :type handshakepattern: HandshakePattern
        :return:
        :rtype: tuple
        """
    def _interpret_as_bob(self, handshakepattern):
        return False

    def modify(self, pattern):
        """
        :param pattern:
        :type pattern: HandshakePattern
        :return:
        :rtype: HandshakePattern
        """
        if not self._is_modifiable(pattern):
            raise ValueError("pattern %s is not modifiable by %s" % (pattern.name, self.name))
        name = pattern.origin_name + ('+'.join(pattern.modifiers + (self.name,)))
        return HandshakePattern(
            name,
            self._get_message_patterns(pattern),
            self._get_initiator_pre_messages(pattern),
            self._get_responder_pre_messages(pattern),
            self._interpret_as_bob(pattern)
        )
