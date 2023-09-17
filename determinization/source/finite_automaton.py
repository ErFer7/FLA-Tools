'''
Módulo de autômatos finitos.
'''


class FiniteAutomaton():

    '''
    Autômato finito.
    '''

    _states: set[str]
    _initial_state: str
    _final_states: set[str]
    _alphabet: set[str]
    _transitions: dict[tuple[str, str], set[str]]

    def __init__(self,
                 states: set[str],
                 initial_state: str,
                 final_states: set[str],
                 alphabet: set[str],
                 transitions: dict[tuple[str, str], set[str]]) -> None:
        self._states = states
        self._initial_state = initial_state
        self._final_states = final_states
        self._alphabet = alphabet
        self._transitions = transitions

    def __str__(self) -> str:
        final_states = '{' + ','.join(sorted(self._final_states)) + '}'
        alphabet = '{' + ','.join(sorted(self._alphabet)) + '}'

        transitions = []

        for (source, symbol), target in self._transitions.items():
            for sub_target in target:
                transitions.append((source, symbol, sub_target))

        sorted_transitions = sorted(transitions, key=lambda x: f'{x[0][1:-1]},{x[1]}')
        processed_transitions = ';'.join([','.join(x) for x in sorted_transitions])

        return f'{len(self._states)};{self._initial_state};{final_states};{alphabet};{processed_transitions}'

    @property
    def initial_state(self) -> str:
        '''
        Retorna o estado inicial.
        '''

        return self._initial_state

    @property
    def final_states(self) -> set[str]:
        '''
        Retorna os estados finais.
        '''

        return self._final_states

    @property
    def alphabet(self) -> set[str]:
        '''
        Retorna o alfabeto.
        '''

        return self._alphabet

    def transition(self, state: str, symbol: str) -> set[str]:
        '''
        Retorna o estado de destino da transição.
        '''

        return self._transitions.get((state, symbol), set())

    def state_epsilon_closure(self, state: str) -> set[str]:
        '''
        Retorna o épsilon-fecho de um estado.
        '''

        epsilon_closure = {state}

        for target_state in self.transition(state, '&'):
            epsilon_closure |= self.state_epsilon_closure(target_state)

        return epsilon_closure

    def epsilon_closure(self) -> dict[str, set[str]]:
        '''
        Retorna o épsilon-fecho de todos os estados.
        '''

        return {state: self.state_epsilon_closure(state) for state in self._states}


class FiniteAutomatonBuilder():

    '''
    Builder.
    '''

    @staticmethod
    def build(raw_data: str) -> FiniteAutomaton:
        '''
        Processa um string de entrada e retorna um autômato finito.
        '''

        data = raw_data.split(';')

        states = set()
        initial_state = data[1]
        final_states = set(data[2][1:-1].split(','))
        alphabet = set(data[3][1:-1].split(','))
        transitions = {}

        for line in data[4:]:
            source, symbol, target = line.split(',')
            states |= {source, target}
            transitions.setdefault((source, symbol), set()).add(target)

        return FiniteAutomaton(states, initial_state, final_states, alphabet, transitions)


class FiniteAutomatonDeterminizer():

    '''
    Determinizador.
    '''

    @staticmethod
    def determinize(finite_automaton: FiniteAutomaton) -> FiniteAutomaton:
        '''
        Determiniza um autômato finito.
        '''

        final_states = set()
        alphabet = {x for x in finite_automaton.alphabet if x != '&'}
        transitions = {}

        epsilon_closure = finite_automaton.epsilon_closure()

        initial_state = FiniteAutomatonDeterminizer.set_to_state(epsilon_closure[finite_automaton.initial_state])
        states = {initial_state}

        unprocessed_states = [initial_state]

        while len(unprocessed_states) > 0:
            source = unprocessed_states.pop(0)

            for symbol in alphabet:
                target = set()

                for state in source[1:-1]:
                    target_set = finite_automaton.transition(state, symbol)

                    for state in target_set:
                        target |= epsilon_closure[state]

                if len(target) == 0:
                    continue

                target_state = FiniteAutomatonDeterminizer.set_to_state(target)

                for state in target_state:
                    if state in finite_automaton.final_states:
                        final_states |= {target_state}

                if target_state not in states:
                    unprocessed_states.append(target_state)

                transitions.setdefault((source, symbol), set()).add(target_state)

                states |= {target_state}

        return FiniteAutomaton(states, initial_state, final_states, alphabet, transitions)

    @staticmethod
    def set_to_state(states: set[str]) -> str:
        '''
        Retorna um estado a partir de um conjunto de estados.
        '''

        return '{' + ''.join(sorted(states)) + '}'
