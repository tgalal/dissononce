import re


class ProtocolParser(object):
    REGEX_PATTERN_NAME_MODIFIERS = r"([A-Z1-9]{1,4})([a-z0-9+]+)*"

    @classmethod
    def parse_handshakepattern(cls, handshake_pattern_name):
        matches = re.search(cls.REGEX_PATTERN_NAME_MODIFIERS, handshake_pattern_name).groups()[:]
        matches = [match for match in matches if match is not None]
        if len(matches) == 2:
            return matches[0], tuple(matches[1].split('+'))
        elif len(matches) == 1:
            return matches[0], ()
        else:
            raise ValueError("Unknown handshake pattern format: %s" % handshake_pattern_name)

    @classmethod
    def parse_protocol_name(cls, protocol_name):
        _, handshake, dh, cipher, hash = protocol_name.split('_')
        return handshake, dh, cipher, hash
