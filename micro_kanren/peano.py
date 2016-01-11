from micro_kanren.sequence import Pair
from micro_kanren.helpers import memoized


#####
# DEFINE PEANO'S ARITHMETIC
#
ZERO, SUCCESSOR = [object() for i in range(2)]


@memoized
def from_integer(integer):
    global ZERO
    global SUCCESSOR

    if integer == 0:
        return ZERO
    else:
        return Pair(SUCCESSOR, from_integer(integer - 1))


@memoized
def to_integer(peano):
    global ZERO

    if peano == ZERO:
        return 0
    else:
        return to_integer(peano.right) + 1


def to_peano(integer):
    return from_integer(integer)


def from_peano(peano):
    return to_integer(peano)

