from dissononce.dh.x25519.x25519 import X25519DH
from dissononce.dh.x448.x448 import X448DH
from dissononce.extras.dh.experimental.secp256k1.secp256k1 import SECP256K1DH

NAME_DH_25519 = '25519'
NAME_DH_448 = '448'
NAME_DH_SECP256K1 = 'secp256k1'

MAP_DH = {
    NAME_DH_25519: X25519DH,
    NAME_DH_448: X448DH,
    NAME_DH_SECP256K1:  SECP256K1DH
}
