from dissononce.extras.meta.protocol.protocol import NoiseProtocol
from dissononce.extras.meta.protocol.factory import NoiseProtocolFactory
from dissononce.dh.private import PrivateKey
from dissononce.dh.dangerous.dh_nogen import NoGenDH
from tests.structs.vector import Vector, VectorVars, VectorMessage

import json
import os
import binascii


class TestVectors(object):
    DIR_VECTORS = os.path.join(os.path.dirname(__file__), 'vectors')
    VECTOR_INIT = 'init'
    VECTOR_RESP = 'resp'

    VECTOR_PROLOGUE = 'prologue'
    VECTOR_STATIC = 'static'
    VECTOR_EPHEMERAL = 'ephemeral'
    VECTOR_REMOTE_STATIC = 'remote_static'
    VECTOR_PSKS = 'psks'

    VECTOR_HANDSHAKE_HASH = 'handshake_hash'
    VECTOR_MESSAGES = 'messages'
    VECTOR_MESSAGE_PAYLOAD = 'payload'
    VECTOR_MESSAGE_CIPHERTEXT = 'ciphertext'

    def pytest_generate_tests(self, metafunc):
        vectors_files = [os.path.join(self.DIR_VECTORS, f) for f in os.listdir(self.DIR_VECTORS) if os.path.isfile(os.path.join(self.DIR_VECTORS, f))]
        vectors = map(self._read_vectors_file, vectors_files)
        relevant_vectors = []
        factory = NoiseProtocolFactory()

        for v in vectors:
           for protocol_vector in v['vectors']:
                try:
                    vector = self._deserialize_vector(protocol_vector)
                    noiseprotocol = factory.get_noise_protocol(protocol_vector['protocol_name'])
                    relevant_vectors.append((noiseprotocol, vector))
                except ValueError:
                    pass

        metafunc.parametrize(('noiseprotocol', 'vector'), relevant_vectors)

    def _read_vectors_file(self, path):
        """
        :param path:
        :type path: str
        :return:
        :rtype: dict
        """
        with open(path, 'r') as f:
            out = json.load(f)
        return out

    def _get_vector_prop(self, vectordict, initiator, prop, default=None):
        """
        :param vectordict:
        :type vectordict: dict
        :param initiator:
        :type initiator: bool | None
        :param prop:
        :type prop: str
        :return:
        :rtype:
        """
        prefix = self.VECTOR_INIT if initiator == True else self.VECTOR_RESP if initiator == False else None
        if prefix is not None:
            property = '%s_%s' % (prefix, prop)
        else:
            property = prop

        value = vectordict[property] if property in vectordict else None
        return value or default

    def _deserialize_vector(self, vectordict):
        """
        :param vectordict:
        :type vectordict: dict
        :return:
        :rtype:
        """
        init_prologue = self._get_vector_prop(vectordict, True, self.VECTOR_PROLOGUE)
        init_static = self._get_vector_prop(vectordict, True, self.VECTOR_STATIC)
        init_ephemeral = self._get_vector_prop(vectordict, True, self.VECTOR_EPHEMERAL)
        init_remote_static = self._get_vector_prop(vectordict, True, self.VECTOR_REMOTE_STATIC)
        init_psks = self._get_vector_prop(vectordict, True, self.VECTOR_PSKS, default=[])

        resp_prologue = self._get_vector_prop(vectordict, False, self.VECTOR_PROLOGUE)
        resp_static = self._get_vector_prop(vectordict, False, self.VECTOR_STATIC)
        resp_ephemeral = self._get_vector_prop(vectordict, False, self.VECTOR_EPHEMERAL)
        resp_remote_static = self._get_vector_prop(vectordict, False, self.VECTOR_REMOTE_STATIC)
        resp_psks = self._get_vector_prop(vectordict, False, self.VECTOR_PSKS, default=[])

        handshake_hash = self._get_vector_prop(vectordict, None, self.VECTOR_HANDSHAKE_HASH)
        messages = self._get_vector_prop(vectordict, None, self.VECTOR_MESSAGES, default=[])

        return Vector (
            init_vectorvars=VectorVars(
                prologue=binascii.unhexlify(init_prologue) if init_prologue else None,
                s=PrivateKey(binascii.unhexlify(init_static)) if init_static else None,
                e=PrivateKey(binascii.unhexlify(init_ephemeral)) if init_ephemeral else None,
                rs=PrivateKey(binascii.unhexlify(init_remote_static)) if init_remote_static else None,
                psks=tuple([binascii.unhexlify(psk) for psk in init_psks])
            ),
            resp_vectorvars=VectorVars(
                prologue=binascii.unhexlify(resp_prologue) if resp_prologue else None,
                s=PrivateKey(binascii.unhexlify(resp_static)) if resp_static else None,
                e=PrivateKey(binascii.unhexlify(resp_ephemeral)) if resp_ephemeral else None,
                rs=PrivateKey(binascii.unhexlify(resp_remote_static)) if resp_remote_static else None,
                psks=tuple([binascii.unhexlify(psk) for psk in resp_psks])
            ),
            handshake_hash=binascii.unhexlify(handshake_hash) if handshake_hash else None,
            messages=[
                VectorMessage(
                    binascii.unhexlify(message[self.VECTOR_MESSAGE_PAYLOAD]),
                    binascii.unhexlify(message[self.VECTOR_MESSAGE_CIPHERTEXT])
                ) for message in messages
            ]
        )

    def test_noise_protocol(self, noiseprotocol, vector):
        """
        :param noiseprotocol:
        :type noiseprotocol: NoiseProtocol
        :type vector: Vector
        :return:
        :rtype:
        """
        init_dh = NoGenDH(noiseprotocol.dh, vector.init_vectorvars.e)
        resp_dh = NoGenDH(noiseprotocol.dh, vector.resp_vectorvars.e)

        init_protocol = NoiseProtocol(noiseprotocol.pattern, init_dh, noiseprotocol.cipher, noiseprotocol.hash)
        resp_protocol = NoiseProtocol(noiseprotocol.pattern, resp_dh, noiseprotocol.cipher, noiseprotocol.hash)

        init_protocol_handshakestate = init_protocol.create_handshakestate()
        resp_protocol_handshakestate = resp_protocol.create_handshakestate()

        init_s = init_dh.generate_keypair(vector.init_vectorvars.s)
        init_rs = noiseprotocol.dh.create_public(vector.init_vectorvars.rs.data) if vector.init_vectorvars.rs else None

        resp_s = resp_dh.generate_keypair(vector.resp_vectorvars.s)
        resp_rs = noiseprotocol.dh.create_public(vector.resp_vectorvars.rs.data) if vector.resp_vectorvars.rs else None

        init_protocol_handshakestate.initialize(
            handshake_pattern=noiseprotocol.pattern,
            initiator=True,
            prologue=vector.init_vectorvars.prologue,
            s=init_s,
            rs=init_rs,
            psks=vector.init_vectorvars.psks
        )

        resp_protocol_handshakestate.initialize(
            handshake_pattern=noiseprotocol.pattern,
            initiator=False,
            prologue=vector.resp_vectorvars.prologue,
            s=resp_s,
            rs=resp_rs,
            psks=vector.resp_vectorvars.psks
        )

        init_cipherstates = None
        resp_cipherstates = None

        transport_messages_offset = 0
        for i in range(0, len(vector.messages)):
            message = vector.messages[i]
            message_buffer = bytearray()
            payload_buffer = bytearray()

            if i % 2 == 0:
                if init_cipherstates is None:
                    init_cipherstates = init_protocol_handshakestate.write_message(message.payload, message_buffer)
                if resp_cipherstates is None:
                    resp_cipherstates = resp_protocol_handshakestate.read_message(bytes(message_buffer), payload_buffer)
            else:
                if resp_cipherstates is None:
                    resp_cipherstates = resp_protocol_handshakestate.write_message(message.payload, message_buffer)
                if init_cipherstates is None:
                    init_cipherstates = init_protocol_handshakestate.read_message(bytes(message_buffer), payload_buffer)

            if init_cipherstates is not None and resp_cipherstates is not None:
                transport_messages_offset = i+1
                break
            else:
                assert message.ciphertext == message_buffer
                assert message.payload == payload_buffer

        if vector.handshake_hash:
            assert init_protocol_handshakestate.symmetricstate.get_handshake_hash() == vector.handshake_hash
            assert resp_protocol_handshakestate.symmetricstate.get_handshake_hash() == vector.handshake_hash

        for i in range(transport_messages_offset, len(vector.messages)):
            message = vector.messages[i]

            if init_protocol.oneway or i % 2 == 0:
                assert message.ciphertext == init_cipherstates[0].encrypt_with_ad(b'', message.payload)
                assert message.payload == resp_cipherstates[0].decrypt_with_ad(b'', message.ciphertext)
            else:
                assert message.ciphertext == resp_cipherstates[1].encrypt_with_ad(b'', message.payload)
                assert message.payload == init_cipherstates[1].decrypt_with_ad(b'', message.ciphertext)
