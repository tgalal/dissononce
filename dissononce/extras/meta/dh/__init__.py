from dissononce.dh.stable.x25519.x25519 import X25519DH
from dissononce.dh.stable.x448.x448 import X448DH

NAME_DH_25519 = '25519'
NAME_DH_448 = '448'

MAP_DH = {
    NAME_DH_25519: X25519DH,
    NAME_DH_448: X448DH
}
