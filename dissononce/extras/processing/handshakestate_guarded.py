from dissononce.extras.processing.handshakestate_forwarder import ForwarderHandshakeState
from transitions import Machine
from transitions.core import MachineError
import logging

logger = logging.getLogger(__name__)
logging.getLogger('transitions').setLevel(logging.INFO)


class GuardedHandshakeState(ForwarderHandshakeState):
    """GuardedHandshakeState wraps an existing HandshakeState to enforce a correct flow of the handshake process.
    This includes making sure the HandshakeState is initialized before usage, and that the flow order of write_message
    and read_message invocations match the HandshakePattern being used. A violation will result in an AssertionError
    getting raised."""
    _STATES = [
        'init',
        'handshake',
        'finish'
    ]
    _TRANSITIONS = [
        ['start', 'init', 'handshake'],
        ['next', 'handshake', '='],
        ['start', 'handshake', '='],
        ['finish', 'handshake', 'finish'],
        ['start', 'finish', 'handshake']
    ]
    _TEMPLATE_PATTERN_STATE_READ = 'read_{pattern}'
    _TEMPLATE_PATTERN_STATE_WRITE = 'write_{pattern}'

    ERROR_TEMPL = "Cannot {bad_method} while in {current} phase."

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
        try:
            self._handshake_machine.start()
        except MachineError as ex:
            raise self._convert_machine_error(ex, 'initialize')

        self._pattern_machine = self._derive_pattern_machine(handshake_pattern, initiator)

        return self._handshakestate.initialize(handshake_pattern, initiator, prologue, s, e, rs, re, psks)

    def write_message(self, payload, message_buffer):
        try:
            self._handshake_machine.next()
            self._pattern_machine.write()
        except MachineError as ex:
            raise self._convert_machine_error(ex, 'write_message')

        result = self._handshakestate.write_message(payload, message_buffer)
        if result is not None:
            self._handshake_machine.finish()
        return result

    def read_message(self, message, payload_buffer):
        try:
            self._handshake_machine.next()
            self._pattern_machine.read()
        except MachineError as ex:
            raise self._convert_machine_error(ex, 'read_message')

        result = self._handshakestate.read_message(message, payload_buffer)
        if result is not None:
            self._handshake_machine.finish()
        return result

    def _convert_machine_error(self, machine_error, bad_method):
        """
        :param machine_error:
        :type machine_error: MachineError
        :param bad_method:
        :type bad_method: str
        :return:
        :rtype:
        """
        if self._handshake_machine.state == 'init':
            current = 'initialize'
        elif self._handshake_machine.state == 'handshake':
            current = 'write_message' if bad_method == 'read_message' else 'write_message'
        else:
            current = self._handshake_machine.state

        error_message = self.ERROR_TEMPL.format(bad_method=bad_method, current=current)
        return AssertionError(error_message)
