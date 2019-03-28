from dissononce.meta.pattern import MAP_PATTERN


class PatternFactory(object):
    def get_pattern(self, name):
        if name in MAP_PATTERN:
            return MAP_PATTERN[name]()
        raise ValueError("Unsupported handshake pattern: %s" % name)
