from itertools import chain
from collections import namedtuple


class Pair(namedtuple('Pair', ('left', 'right'))):
    '''Pair is a named-tuple subclass that can be converted to string'''
    def __str__(self):
        return "({}, {})".format(self.left, self.right if self.right != Sequence.EMPTY else "*")


class Sequence:
    '''Defines operations on sequences of pairs'''
    # A constant that denotes the end of a sequence
    EMPTY = object()

    @classmethod
    def from_list(cls, a_list):
        '''Converts a Python list to a sequence of nested Pair objects'''
        if not a_list:
            return cls.EMPTY
        elif not isinstance(a_list, list):
            raise TypeError("parameter needs to be a list object")
        else:
            first, *rest = a_list
            return Pair(first, cls.from_list(rest))

    @classmethod
    def to_list(cls, a_sequence):
        '''Converts a sequence of nested Pair objects to a Python list'''
        if a_sequence == cls.EMPTY:
            return []
        if not isinstance(a_sequence, Pair):
            raise TypeError("The parameter is not a Pair object.")
        else:
            first, rest = a_sequence.left, a_sequence.right
            return list(chain.from_iterable([first, Sequence.to_list(rest)]))

