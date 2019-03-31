import json
import os
import binascii

from dissononce.protocol import NoiseProtocol
from dissononce.meta.protocol.factory import NoiseProtocolFactory
from dissononce.dh.private import PrivateKey

from tests.dh_nogen import NoGenDH


class TestVectors(object):
    DIR_VECTORS = os.path.join(os.path.dirname(__file__), 'vectors')

    def pytest_generate_tests(self, metafunc):
        vectors_files = [os.path.join(self.DIR_VECTORS, f) for f in os.listdir(self.DIR_VECTORS) if os.path.isfile(os.path.join(self.DIR_VECTORS, f))]
        vectors = map(self._read_vectors_file, vectors_files)
        relevant_vectors = []
        factory = NoiseProtocolFactory()

        for v in vectors:
           for protocol_vectors in v['vectors']:
                try:
                    noiseprotocol = factory.get_noise_protocol(protocol_vectors['protocol_name'])
                    relevant_vectors.append((noiseprotocol, protocol_vectors))
                except ValueError:
                    pass

        metafunc.parametrize(('noiseprotocol', 'protocol_vectors'), relevant_vectors)

    def _get_vectors(self, protocolname, path):
        vectors = self._read_vectors_file(path)
        assert protocolname in vectors['vectors']
        return vectors['vectors'][protocolname]

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

    def test_noise_protocol(self, noiseprotocol, protocol_vectors):
        """
        :param noiseprotocol:
        :type noiseprotocol: NoiseProtocol
        :return:
        :rtype:
        """
        init_dh = NoGenDH(noiseprotocol.dh, PrivateKey(binascii.unhexlify(protocol_vectors['init_ephemeral'])))
        resp_dh = NoGenDH(
            noiseprotocol.dh,
            PrivateKey(
                binascii.unhexlify(protocol_vectors['resp_ephemeral'])
            ) if 'resp_ephemeral' in protocol_vectors else None
        )

        init_protocol = NoiseProtocol(noiseprotocol.pattern, init_dh, noiseprotocol.cipher, noiseprotocol.hash)
        resp_protocol = NoiseProtocol(noiseprotocol.pattern, resp_dh, noiseprotocol.cipher, noiseprotocol.hash)

        init_prologue = binascii.unhexlify(protocol_vectors['init_prologue'])
        init_s = init_dh.generate_keypair(PrivateKey(binascii.unhexlify(protocol_vectors['init_static']))) if 'init_static' in protocol_vectors else None
        init_rs = noiseprotocol.dh.create_public(binascii.unhexlify(protocol_vectors['init_remote_static'])) if 'init_remote_static' in protocol_vectors else None
        init_psks = [binascii.unhexlify(vectors_psks) for vectors_psks in protocol_vectors['init_psks']] if 'init_psks' in protocol_vectors else None

        resp_prologue = binascii.unhexlify(protocol_vectors['resp_prologue'])
        resp_s = resp_dh.generate_keypair(PrivateKey(binascii.unhexlify(protocol_vectors['resp_static']))) if 'resp_static' in protocol_vectors else None
        resp_rs = noiseprotocol.dh.create_public(binascii.unhexlify(protocol_vectors['resp_remote_static'])) if 'resp_remote_static' in protocol_vectors else None
        resp_psks = [binascii.unhexlify(vectors_psks) for vectors_psks in protocol_vectors['resp_psks']] if 'resp_psks' in protocol_vectors else None

        init_protocol.handshakestate.initialize(
            handshake_pattern=noiseprotocol.pattern,
            initiator=True,
            prologue=init_prologue,
            s=init_s,
            rs=init_rs,
            psks=init_psks
        )

        resp_protocol.handshakestate.initialize(
            handshake_pattern=noiseprotocol.pattern,
            initiator=False,
            prologue=resp_prologue,
            s=resp_s,
            rs=resp_rs,
            psks=resp_psks
        )

        init_cipherstates = None
        resp_cipherstates = None

        transport_messages_offset = 0
        for i in range(0, len(protocol_vectors['messages'])):
            message = protocol_vectors['messages'][i]
            payload = binascii.unhexlify(message['payload'])
            ciphertext = binascii.unhexlify(message['ciphertext'])
            message_buffer = bytearray()
            payload_buffer = bytearray()

            if i % 2 == 0:
                if init_cipherstates is None:
                    init_cipherstates = init_protocol.handshakestate.write_message(payload, message_buffer)
                if resp_cipherstates is None:
                    resp_cipherstates = resp_protocol.handshakestate.read_message(bytes(message_buffer), payload_buffer)
            else:
                if resp_cipherstates is None:
                    resp_cipherstates = resp_protocol.handshakestate.write_message(payload, message_buffer)
                if init_cipherstates is None:
                    init_cipherstates = init_protocol.handshakestate.read_message(bytes(message_buffer), payload_buffer)

            if init_cipherstates is not None and resp_cipherstates is not None:
                transport_messages_offset = i+1
                break
            else:
                assert ciphertext == message_buffer
                assert payload == payload_buffer

        if 'handshake_hash' in protocol_vectors:
            assert init_protocol.symmetricstate.get_handshake_hash() == binascii.unhexlify(protocol_vectors['handshake_hash'])
            assert init_protocol.symmetricstate.get_handshake_hash() == binascii.unhexlify(protocol_vectors['handshake_hash'])

        for i in range(transport_messages_offset, len(protocol_vectors['messages'])):
            message = protocol_vectors['messages'][i]
            payload = binascii.unhexlify(message['payload'])
            ciphertext = binascii.unhexlify(message['ciphertext'])

            if init_protocol.oneway or i % 2 == 0:
                assert ciphertext == init_cipherstates[0].encrypt_with_ad(b'', payload)
                assert payload == resp_cipherstates[0].decrypt_with_ad(b'', ciphertext)
            else:
                assert ciphertext == resp_cipherstates[1].encrypt_with_ad(b'', payload)
                assert payload == init_cipherstates[1].decrypt_with_ad(b'', ciphertext)
