class VectorVars(object):
    def __init__(self, prologue, s, e, rs, psks):
        self._prologue = prologue
        self._s = s
        self._e = e
        self._rs = rs
        self._psks = psks or tuple()

    @property
    def prologue(self):
        return self._prologue

    @property
    def s(self):
        return self._s

    @property
    def e(self):
        return self._e

    @property
    def rs(self):
        return self._rs

    @property
    def psks(self):
        return self._psks
