'''
Módulo de autômatos finitos.
'''

from copy import deepcopy


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

        sorted_transitions = sorted(transitions, key=lambda x: (x[0].strip('{}'), x[1]))
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

    def source_states(self, state: str, symbol: str | None = None) -> set[str]:
        '''
        Retorna todos os estados de origem de uma transição.
        '''

        items = self._transitions.items()

        if symbol is None:
            return {source for (source, _), target in items if state in target}

        return {source for (source, selected_symbol), target in items if state in target and symbol == selected_symbol}

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


class FiniteAutomatonMinimizer():

    '''
    Minimizador.
    '''

    @staticmethod
    def minimize(finite_automaton: FiniteAutomaton) -> FiniteAutomaton:
        '''
        Minimiza um autômato finito determinístico.
        '''

        reachable_states = FiniteAutomatonMinimizer.filter_unreachable_states(finite_automaton)
        reachable_final_states = finite_automaton.final_states & reachable_states
        live_states = reachable_final_states.copy()

        FiniteAutomatonMinimizer.filter_dead_states(finite_automaton, live_states, live_states)

        equivalence_classes = FiniteAutomatonMinimizer.refine_equivalence_classes(finite_automaton,
                                                                                  live_states,
                                                                                  reachable_final_states)

        states = set(map(lambda x: sorted(x)[0], equivalence_classes))
        final_states = {state for state in states if state in reachable_final_states}
        alphabet = finite_automaton.alphabet
        transitions = {}

        for source in states:
            for symbol in alphabet:
                old_targets = finite_automaton.transition(source, symbol)

                for equivalence_class in equivalence_classes:
                    if len(old_targets & equivalence_class) > 0:
                        transitions.setdefault((source, symbol), set()).add(sorted(equivalence_class)[0])

        return FiniteAutomaton(states, finite_automaton.initial_state, final_states, alphabet, transitions)

    @staticmethod
    def filter_unreachable_states(finite_automaton: FiniteAutomaton) -> set[str]:
        '''
        Remove estados inalcançáveis.
        '''

        reachable_states = {finite_automaton.initial_state}
        unprocessed_states = [finite_automaton.initial_state]

        while len(unprocessed_states) > 0:
            source = unprocessed_states.pop(0)

            for symbol in finite_automaton.alphabet:
                for target in finite_automaton.transition(source, symbol):
                    if target not in reachable_states:
                        reachable_states |= {target}
                        unprocessed_states.append(target)

        return reachable_states

    @staticmethod
    def filter_dead_states(finite_automaton: FiniteAutomaton,
                           visited_live_states: set[str],
                           live_states: set[str]) -> None:
        '''
        Remove estados mortos.
        '''

        new_live_states = set()

        for state in live_states:
            new_live_states |= finite_automaton.source_states(state)

        new_live_states -= visited_live_states
        visited_live_states |= new_live_states

        if len(new_live_states) > 0:
            FiniteAutomatonMinimizer.filter_dead_states(finite_automaton, visited_live_states, new_live_states)

    @staticmethod
    def refine_equivalence_classes(finite_automaton: FiniteAutomaton,
                                   live_states: set[str],
                                   final_states: set[str]) -> list[set[str]]:
        '''
        Refina as classes de equivalência.
        '''

        equivalence_classes = [live_states - final_states, final_states]
        equivalence_classes_temp = deepcopy(equivalence_classes)

        while len(equivalence_classes_temp) > 0:
            equivalence_class_temp = equivalence_classes_temp.pop(0)

            for symbol in finite_automaton.alphabet:
                source_states = set()

                for state in equivalence_class_temp:
                    source_states |= finite_automaton.source_states(state, symbol)

                index = 0
                while index < len(equivalence_classes):
                    equivalence_class = equivalence_classes[index]

                    if len(source_states & equivalence_class) > 0 and len(equivalence_class - source_states) > 0:
                        # Set se refere ao conjunto de estados em uma classe de equivalência.
                        old_set_index = equivalence_classes.index(equivalence_class)
                        intersected_set = source_states & equivalence_class
                        subtracted_set = equivalence_class - source_states
                        index += 1

                        equivalence_classes[old_set_index] = intersected_set
                        equivalence_classes.insert(old_set_index + 1, subtracted_set)

                        if equivalence_class in equivalence_classes_temp:
                            old_set_temp_index = equivalence_classes_temp.index(equivalence_class)

                            equivalence_classes_temp[old_set_temp_index] = intersected_set
                            equivalence_classes_temp.insert(old_set_temp_index, subtracted_set)
                        else:
                            if len(intersected_set) <= len(subtracted_set):
                                equivalence_classes_temp.append(intersected_set)
                            else:
                                equivalence_classes_temp.append(subtracted_set)

                    index += 1

        return equivalence_classes
