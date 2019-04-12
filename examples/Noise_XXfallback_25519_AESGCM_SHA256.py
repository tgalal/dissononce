"""
The following demonstrates a Noise_IK_25519_AESGCM_SHA256 that fails during handshake, making initiator and responder
switch to Noise_XXfallback_25519_AESGCM_SHA256
"""
from dissononce.processing.impl.handshakestate import HandshakeState
from dissononce.extras.processing.handshakestate_switchable import SwitchableHandshakeState
from dissononce.processing.impl.symmetricstate import SymmetricState
from dissononce.processing.impl.cipherstate import CipherState
from dissononce.processing.handshakepatterns.interactive.XX import XXHandshakePattern
from dissononce.processing.handshakepatterns.interactive.IK import IKHandshakePattern
from dissononce.processing.modifiers.fallback import FallbackPatternModifier
from dissononce.cipher.aesgcm import AESGCMCipher
from dissononce.dh.x25519.x25519 import X25519DH
from dissononce.hash.sha256 import SHA256Hash
from dissononce.exceptions.decrypt import DecryptFailedException
import dissononce, logging

if __name__ == "__main__":
    dissononce.logger.setLevel(logging.DEBUG)
    # setup initiator and responder variables
    alice_s = X25519DH().generate_keypair()
    alice_rs = X25519DH().generate_keypair().public
    bob_s = X25519DH().generate_keypair()

    # prepare handshakestate objects for initiator and responder
    alice_handshakestate = SwitchableHandshakeState(HandshakeState(
        SymmetricState(
            CipherState(
                AESGCMCipher()
            ),
            SHA256Hash()
        ),
        X25519DH()
    ))
    bob_handshakestate = SwitchableHandshakeState(HandshakeState(
        SymmetricState(
            CipherState(
                AESGCMCipher()
            ),
            SHA256Hash()
        ),
        X25519DH()
    ))
    # initialize handshakestate objects
    alice_handshakestate.initialize(IKHandshakePattern(), True, b'', s=alice_s, rs=alice_rs)
    bob_handshakestate.initialize(IKHandshakePattern(), False, b'', s=bob_s)

    # -> e, es, s, ss
    message_buffer = bytearray()
    alice_handshakestate.write_message(b'', message_buffer)
    try:
        bob_handshakestate.read_message(bytes(message_buffer), bytearray())
    except DecryptFailedException:
        # bob failed to read alice's message, possibly because alice used wrong static keys for bob, will now fallback
        # to XX
        bob_handshakestate.switch(FallbackPatternModifier().modify(XXHandshakePattern()), False, b'', s=bob_s)

    # <- e, ee, s, es
    message_buffer = bytearray()
    bob_handshakestate.write_message(b'', message_buffer)

    try:
        # alice doesn't yet know about the XX fallback switch and still expects IK's (e, ee, se) pattern
        alice_handshakestate.read_message(bytes(message_buffer), bytearray())
    except DecryptFailedException:
        # alice failed to read bob's message. but alice and bob had a pre-agreement that if will happen if bob for
        # whatever reason descides to fall back to XX, an therefore so must alice
        alice_handshakestate.switch(FallbackPatternModifier().modify(XXHandshakePattern()), True, b'', s=alice_s)

    # alice should now successfuly read bob's message, which includes bob's new static public key.
    alice_handshakestate.read_message(bytes(message_buffer), bytearray())

    # -> s, se
    message_buffer = bytearray()
    alice_cipherstates = alice_handshakestate.write_message(b'', message_buffer)
    bob_cipherstates = bob_handshakestate.read_message(bytes(message_buffer), bytearray())

    # transport phase
    # alice to bob
    ciphertext = alice_cipherstates[0].encrypt_with_ad(b'', b'Hello')
    plaintext = bob_cipherstates[0].decrypt_with_ad(b'', ciphertext)
    assert plaintext == b'Hello'

    # bob to alice
    ciphertext = bob_cipherstates[1].encrypt_with_ad(b'', b'World')
    plaintext = alice_cipherstates[1].decrypt_with_ad(b'', ciphertext)
    assert plaintext == b'World'
