"""
The following demonstrates a Noise_IK_25519_AESGCM_SHA256 that fails during handshake, making initiator and responder
switch to Noise_IK_25519_AESGCM_SHA256
"""
from dissononce.processing.impl.handshakestate import HandshakeState
from dissononce.processing.impl.symmetricstate import SymmetricState
from dissononce.processing.impl.cipherstate import CipherState
from dissononce.processing.handshakepatterns.interactive.IK import IKHandshakePattern
from dissononce.cipher.aesgcm import AESGCMCipher
from dissononce.dh.x25519.x25519 import X25519DH
from dissononce.hash.sha256 import SHA256Hash
import dissononce, logging


if __name__ == "__main__":
    dissononce.logger.setLevel(logging.DEBUG)
    # setup initiator and responder variables
    alice_s = X25519DH().generate_keypair()
    bob_s = X25519DH().generate_keypair()

    # prepare handshakestate objects for initiator and responder
    alice_handshakestate = HandshakeState(
        SymmetricState(
            CipherState(
                AESGCMCipher()
            ),
            SHA256Hash()
        ),
        X25519DH()
    )
    bob_handshakestate = HandshakeState(
        SymmetricState(
            CipherState(
                AESGCMCipher()
            ),
            SHA256Hash()
        ),
        X25519DH()
    )
    # initialize handshakestate objects
    alice_handshakestate.initialize(IKHandshakePattern(), True, b'', s=alice_s, rs=bob_s.public)
    bob_handshakestate.initialize(IKHandshakePattern(), False, b'', s=bob_s)

    # -> e, es, s, ss
    message_buffer = bytearray()
    alice_handshakestate.write_message(b'', message_buffer)
    bob_handshakestate.read_message(bytes(message_buffer), bytearray())

    # <- e, ee, se
    message_buffer = bytearray()
    bob_cipherstates = bob_handshakestate.write_message(b'', message_buffer)
    alice_cipherstates = alice_handshakestate.read_message(bytes(message_buffer), bytearray())

    # transport phase
    # alice to bob
    ciphertext = alice_cipherstates[0].encrypt_with_ad(b'', b'Hello')
    plaintext = bob_cipherstates[0].decrypt_with_ad(b'', ciphertext)
    assert plaintext == b'Hello'

    # bob to alice
    ciphertext = bob_cipherstates[1].encrypt_with_ad(b'', b'World')
    plaintext = alice_cipherstates[1].decrypt_with_ad(b'', ciphertext)
    assert plaintext == b'World'
