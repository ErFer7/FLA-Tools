'''
Árvore.
'''

from typing import Any


class ParseNode():

    '''
    Nó.
    '''

    _value: str
    _index: int | None
    _left: Any
    _right: Any
    _nullable: bool
    _firstpos: set[int]
    _lastpos: set[int]

    def __init__(self, value: str, left: Any, right: Any, index: int | None = None):
        self._value = value
        self._index = index
        self._left = left
        self._right = right
        self._nullable = False
        self._firstpos = set()
        self._lastpos = set()

    def __str__(self) -> str:
        result = ''

        if self._left is not None:
            result += f'({str(self._left)})-'

        result += f'{self._value}['

        if self._index is not None:
            result += f'{self._index} / '

        result += f'{self._nullable} / {self._firstpos} / {self._lastpos}]'

        if self._right is not None:
            result += f'-({str(self._right)})'

        return result

    @property
    def nullable(self) -> bool:
        '''
        Getter para nullable.
        '''

        return self._nullable

    @property
    def firstpos(self) -> set[int]:
        '''
        Getter para firstpos.
        '''

        return self._firstpos

    @property
    def lastpos(self) -> set[int]:
        '''
        Getter para lastpos.
        '''

        return self._lastpos

    def calculate_nullable(self) -> None:
        '''
        Calcula o valor de nullable.
        '''

        if self._left is not None:
            self._left.calculate_nullable()

        if self._right is not None:
            self._right.calculate_nullable()

        match self._value:
            case '*':
                self._nullable = True
            case '.':
                self._nullable = self._left.nullable and self._right.nullable
            case '|':
                self._nullable = self._left.nullable or self._right.nullable
            case '&':
                self._nullable = True
            case _:
                self._nullable = False

    def calculate_firstpos(self) -> None:
        '''
        Calcula o valor de firstpos.
        '''

        if self._left is not None:
            self._left.calculate_firstpos()

        if self._right is not None:
            self._right.calculate_firstpos()

        match self._value:
            case '*':
                self._firstpos = self._left.firstpos.copy()
            case '.':
                if self._left.nullable:
                    self._firstpos = self._left.firstpos | self._right.firstpos
                else:
                    self._firstpos = self._left.firstpos.copy()
            case '|':
                self._firstpos = self._left.firstpos | self._right.firstpos
            case '&':
                self._firstpos = set()
            case _:
                self._firstpos = {self._index}  # type: ignore

    def calculate_lastpos(self) -> None:
        '''
        Calcula o valor de lastpos.
        '''

        if self._left is not None:
            self._left.calculate_lastpos()

        if self._right is not None:
            self._right.calculate_lastpos()

        match self._value:
            case '*':
                self._lastpos = self._left.lastpos.copy()
            case '.':
                if self._right.nullable:
                    self._lastpos = self._left.lastpos | self._right.lastpos
                else:
                    self._lastpos = self._right.lastpos.copy()
            case '|':
                self._lastpos = self._left.lastpos | self._right.lastpos
            case '&':
                self._lastpos = set()
            case _:
                self._lastpos = {self._index}  # type: ignore

    def calculate_followpos(self, followpos: dict[int, set[int]]) -> None:
        '''
        Calcula o valor de followpos.
        '''

        if self._left is not None:
            self._left.calculate_followpos(followpos)

        if self._right is not None:
            self._right.calculate_followpos(followpos)

        match self._value:
            case '.':
                for position in self._left.lastpos:
                    followpos[position] |= self._right.firstpos
            case '*':
                for position in self._lastpos:
                    followpos[position] |= self._firstpos


class ParseTree():

    '''
    Árvore.
    '''

    _root: ParseNode | None
    _last_symbol_index: int
    _symbols: set[str]
    _positions_symbols: dict[int, str]

    def __init__(self, postfixed_regex: list[str | ParseNode]):
        self._root = None
        self._symbols = set()
        self._positions_symbols = {}
        symbol_index = 0

        while len(postfixed_regex) > 1:
            index = 0

            while index < len(postfixed_regex):
                if postfixed_regex[index] == '*':
                    if isinstance(postfixed_regex[index - 1], ParseNode):
                        self._root = ParseNode(postfixed_regex[index], postfixed_regex[index - 1], None)  # type: ignore
                    else:
                        subnode = None

                        if postfixed_regex[index - 1] != '&':
                            symbol_index += 1
                            self._symbols |= {postfixed_regex[index - 1]}
                            self._positions_symbols[symbol_index] = postfixed_regex[index - 1]
                            subnode = ParseNode(postfixed_regex[index - 1], None, None, symbol_index)  # type: ignore
                        else:
                            subnode = ParseNode(postfixed_regex[index - 1], None, None)  # type: ignore

                        self._root = ParseNode(postfixed_regex[index], subnode, None)  # type: ignore

                    postfixed_regex.pop(index)
                    postfixed_regex.pop(index - 1)
                    postfixed_regex.insert(index - 1, self._root)

                    continue
                elif postfixed_regex[index] in ('.', '|'):
                    if isinstance(postfixed_regex[index - 2], ParseNode) and isinstance(postfixed_regex[index - 1], ParseNode):
                        self._root = ParseNode(postfixed_regex[index], postfixed_regex[index - 2], postfixed_regex[index - 1])  # type: ignore
                    elif isinstance(postfixed_regex[index - 2], ParseNode):
                        subnode = None

                        if postfixed_regex[index - 1] != '&':
                            symbol_index += 1
                            self._symbols |= {postfixed_regex[index - 1]}
                            self._positions_symbols[symbol_index] = postfixed_regex[index - 1]
                            subnode = ParseNode(postfixed_regex[index - 1], None, None, symbol_index)  # type: ignore
                        else:
                            subnode = ParseNode(postfixed_regex[index - 1], None, None)  # type: ignore

                        self._root = ParseNode(postfixed_regex[index], postfixed_regex[index - 2], subnode)  # type: ignore
                    elif isinstance(postfixed_regex[index - 1], ParseNode):
                        subnode = None

                        if postfixed_regex[index - 2] != '&':
                            symbol_index += 1
                            self._symbols |= {postfixed_regex[index - 2]}
                            self._positions_symbols[symbol_index] = postfixed_regex[index - 2]
                            subnode = ParseNode(postfixed_regex[index - 2], None, None, symbol_index)  # type: ignore
                        else:
                            subnode = ParseNode(postfixed_regex[index - 2], None, None)  # type: ignore

                        self._root = ParseNode(postfixed_regex[index], subnode, postfixed_regex[index - 1])  # type: ignore
                    else:
                        left_subnode = None

                        if postfixed_regex[index - 2] != '&':
                            symbol_index += 1
                            self._symbols |= {postfixed_regex[index - 2]}
                            self._positions_symbols[symbol_index] = postfixed_regex[index - 2]
                            left_subnode = ParseNode(postfixed_regex[index - 2], None, None, symbol_index)  # type: ignore
                        else:
                            left_subnode = ParseNode(postfixed_regex[index - 2], None, None)  # type: ignore

                        right_subnode = None

                        if postfixed_regex[index - 1] != '&':
                            symbol_index += 1
                            self._symbols |= {postfixed_regex[index - 1]}
                            self._positions_symbols[symbol_index] = postfixed_regex[index - 1]
                            right_subnode = ParseNode(postfixed_regex[index - 1], None, None, symbol_index)  # type: ignore
                        else:
                            right_subnode = ParseNode(postfixed_regex[index - 1], None, None)  # type: ignore

                        self._root = ParseNode(postfixed_regex[index], left_subnode, right_subnode)  # type: ignore

                    postfixed_regex.pop(index)
                    postfixed_regex.pop(index - 1)
                    postfixed_regex.pop(index - 2)
                    postfixed_regex.insert(index - 2, self._root)
                    index -= 1

                    continue

                index += 1

        self._symbols -= {'#'}
        self._last_symbol_index = symbol_index

    def __str__(self) -> str:
        return str(self._root)

    @property
    def root(self) -> ParseNode | None:
        '''
        Getter para root.
        '''

        return self._root

    @property
    def symbols(self) -> set[str]:
        '''
        Getter para symbols.
        '''

        return self._symbols

    @property
    def positions_symbols(self) -> dict[int, str]:
        '''
        Getter para positions_symbols.
        '''

        return self._positions_symbols

    def calculate_nullable(self) -> None:
        '''
        Calcula os valores de nullable.
        '''

        self._root.calculate_nullable()  # type: ignore

    def calculate_firstpos(self) -> None:
        '''
        Calcula os valores de firstpos.
        '''

        self._root.calculate_firstpos()  # type: ignore

    def calculate_lastpos(self) -> None:
        '''
        Calcula os valores de lastpos.
        '''

        self._root.calculate_lastpos()  # type: ignore

    def calculate_followpos(self) -> dict[int, set[int]]:
        '''
        Calcula os valores de followpos.
        '''

        self.calculate_nullable()
        self.calculate_firstpos()
        self.calculate_lastpos()

        print(self)

        followpos = {index: set() for index in range(1, self._last_symbol_index + 1)}

        self._root.calculate_followpos(followpos)  # type: ignore

        return followpos
