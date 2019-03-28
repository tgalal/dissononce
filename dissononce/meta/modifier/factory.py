from dissononce.meta.modifier import MAP_MODIFIER


class ModifierFactory(object):
    def get_modifier(self, name):
        if name in MAP_MODIFIER:
            return MAP_MODIFIER[name]()
        raise ValueError("Unsupported modifier: %s" % name)
