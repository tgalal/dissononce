class HandshakePattern(object):

    TEMPLATE_REPR = "{name}:\n{patterns}"
    TEMPLATE_REPR_PATTERNS_WITH_PRE = "{pre_patterns}\n  ...\n{message_patterns}"
    TEMPLATE_REPR_MESSAGE_SEND = "  -> {tokens}"
    TEMPLATE_REPR_MESSAGE_RECV = "  <- {tokens}"

    def __init__(self,
                 name,
                 message_patterns,
                 initiator_pre_messages=None,
                 responder_pre_message_pattern=None,
                 interpret_as_bob=False
                 ):
        """
        :param name:
        :type name: str
        :param message_pattern:
        :type message_pattern: tuple[tuple[str]]
        :param initiator_pre_messages:
        :type initiator_pre_messages: tuple[str]
        :param responder_pre_message_pattern:
        :type responder_pre_message_pattern: tuple[str]
        """
        self._name = name # type: str
        self._message_patterns = message_patterns # type: tuple[tuple[str]]
        self._initiator_pre_message_pattern = initiator_pre_messages or tuple() # type: tuple[str]
        self._responder_pre_message_pattern = responder_pre_message_pattern or tuple() # type: tuple[str]
        self._interpret_as_bob = interpret_as_bob # type: bool

    def __str__(self):
        out_pre = []
        out_messages = []
        templ_send = self.__class__.TEMPLATE_REPR_MESSAGE_SEND
        templ_recv = self.__class__.TEMPLATE_REPR_MESSAGE_RECV

        for pattern in self._initiator_pre_message_pattern:
            out_pre.append(templ_send.format(tokens = ", ".join(pattern)))

        for pattern in self.responder_pre_message_pattern:
            out_pre.append(templ_recv.format(tokens = ", ".join(pattern)))

        for i in range(0, len(self.message_patterns)):
            use_send = i % 2 == 0
            if self.interpret_as_bob:
                use_send = not use_send
            template = templ_send if use_send else templ_recv
            out_messages.append(template.format(tokens=", ".join(self.message_patterns[i])))

        message_patterns_formatted = "\n".join(out_messages)
        if len(out_pre):
            pre_formatted = "\n".join(out_pre)
            patterns_formatted = self.__class__.TEMPLATE_REPR_PATTERNS_WITH_PRE.format(pre_patterns=pre_formatted, message_patterns=message_patterns_formatted)
        else:
            patterns_formatted = message_patterns_formatted

        return self.__class__.TEMPLATE_REPR.format(name=self.name, patterns=patterns_formatted)

    @property
    def name(self):
        return self._name

    @property
    def interpret_as_bob(self):
        return self._interpret_as_bob

    @property
    def message_patterns(self):
        return self._message_patterns

    @property
    def initiator_pre_message_pattern(self):
        return self._initiator_pre_message_pattern

    @property
    def responder_pre_message_pattern(self):
        return self._responder_pre_message_pattern
