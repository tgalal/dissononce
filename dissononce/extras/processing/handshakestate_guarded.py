from dissononce.extras.processing.handshakestate_forwarder import ForwarderHandshakeState

from transitions import Machine
import logging

logger = logging.getLogger(__name__)
logging.getLogger('transitions').setLevel(logging.INFO)


class GuardedHandshakeState(ForwarderHandshakeState):

    _STATES = [
        'init',
        'handshake',
        'finish'
    ]
    _TRANSITIONS = [
        ['start', 'init', 'handshake'],
        ['next', 'handshake', '='],
        ['reset', 'handshake', 'init'],
        ['finish', 'handshake', 'finish'],
        ['init', 'finish', 'handshake']
    ]
    _TEMPLATE_PATTERN_STATE_READ = 'read_{pattern}'
    _TEMPLATE_PATTERN_STATE_WRITE = 'write_{pattern}'

    def __init__(self, handshakestate):
        """
        :param handshakestate:
        :type handshakestate: HandshakeState
        """
        super(GuardedHandshakeState, self).__init__(handshakestate)
        self._handshake_machine = Machine(
            states=self._STATES,
            transitions=self._TRANSITIONS,
            initial='init'
        )  # type: Machine
        self._pattern_machine = None  # type: Machine

    def _derive_pattern_machine(self, handshake_pattern, initiator):
        """
        :param pattern:
        :type pattern: HandshakePattern
        :return:
        :rtype: Machine
        """
        states = ['finish']
        transitions = []
        prev_state = None
        for i in range(0, len(handshake_pattern.message_patterns)):
            read_phase = i % 2 == 0
            if handshake_pattern.interpret_as_bob:
                read_phase = not read_phase
            if not initiator:
                read_phase = not read_phase
            message_pattern = handshake_pattern.message_patterns[i]
            pattern_str = "_".join(message_pattern)
            template = self._TEMPLATE_PATTERN_STATE_WRITE if read_phase else self._TEMPLATE_PATTERN_STATE_READ

            state = template.format(pattern=pattern_str)
            if prev_state is not None:
                action = 'read' if read_phase else 'write'
                transitions.append([action, prev_state, state])

            if i == len(handshake_pattern.message_patterns) - 1:
                transitions.append(['write' if read_phase else 'read', state, 'finish'])

            states.append(state)
            prev_state = state

        return Machine(states=states, transitions=transitions, initial=states[1])

    def initialize(self, handshake_pattern, initiator, prologue, s=None, e=None, rs=None, re=None, psks=None):
        if self._handshake_machine.state == 'handshake':
            self._handshake_machine.reset()

        self._handshake_machine.start()
        self._pattern_machine = self._derive_pattern_machine(handshake_pattern, initiator)

        return self._handshakestate.initialize(handshake_pattern, initiator, prologue, s, e, rs, re, psks)

    def write_message(self, payload, message_buffer):
        self._handshake_machine.next()
        self._pattern_machine.write()
        result = self._handshakestate.write_message(payload, message_buffer)
        if result is not None:
            self._handshake_machine.finish()
        return result

    def read_message(self, message, payload_buffer):
        self._handshake_machine.next()
        self._pattern_machine.read()
        result = self._handshakestate.read_message(message, payload_buffer)
        if result is not None:
            self._handshake_machine.finish()
        return result
