
from dissononce.dh import public


class PublicKey(public.PublicKey):
    def __init__(self, data):
        super(PublicKey, self).__init__(33, data)
