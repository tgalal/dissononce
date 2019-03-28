from dissononce.meta.hash import MAP_HASH


class HashFactory(object):
    def get_hash(self, name):
        if name in MAP_HASH:
            return MAP_HASH[name]()
        raise ValueError("Unsupported Hash: %s" % name)
