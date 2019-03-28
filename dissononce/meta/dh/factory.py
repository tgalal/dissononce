from dissononce.meta.dh import MAP_DH


class DHFactory(object):
    def get_dh(self, name):
        if name in MAP_DH:
            return MAP_DH[name]()
        raise ValueError("Unsupported DH: %s" % name)
