from dissononce.hash.stable.sha256 import SHA256Hash
from dissononce.hash.stable.sha512 import SHA512Hash
from dissononce.hash.stable.blake2s import Blake2sHash
from dissononce.hash.stable.blake2b import Blake2bHash


NAME_SHA256 = 'SHA256'
NAME_SHA512 = 'SHA512'
NAME_BLAKE2S = 'BLAKE2s'
NAME_BLAKE2B = 'BLAKE2b'

MAP_HASH = {
    NAME_SHA256: SHA256Hash,
    NAME_SHA512: SHA512Hash,
    NAME_BLAKE2S: Blake2sHash,
    NAME_BLAKE2B: Blake2bHash
}
