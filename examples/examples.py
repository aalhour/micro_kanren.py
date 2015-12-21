import itertools
from micro_kanren.everything import *


###
# States in micro are immutable
EMPTY_STATE = State()


#####
# Assignment with a state of multi-variables.
#
print("[*] Problem: x = 5.")
print("[*] Pursue from a state with variables (x, y, z), and no values...")

beginning_state, (x, y, z) = State().create_variables(['x', 'y', 'z'])
goal = Goal.equal(x, 5)
states = goal.pursue_in(beginning_state)

print(beginning_state)
for state in states:
    print(state)

print('\r\n')


#####
# Assignment from an empty state.
#
print("[*] Problem: x = 5")
print("[*] Pursue from an empty state...")

goal = Goal.with_variables(lambda x: Goal.equal(x, 5))
states = goal.pursue_in(EMPTY_STATE)

print(EMPTY_STATE)
for state in states:
    print(state)

print('\r\n')


#####
# Either-Or conditions
#
print("[*] Problem: Either x = 5 Or y = 6.")
print("[*] Pursue from an empty state...")

goal = Goal.with_variables(lambda x, y:
    Goal.either(
        Goal.equal(x, 5),
        Goal.equal(y, 6)))
states = goal.pursue_in(EMPTY_STATE)

print(EMPTY_STATE)
for state in states:
    print(state)            # This Either condition gives two states as a result

print('\r\n')


#####
# And conditions
#
print("[*] Problem: Both x = 5 And y = 7.")
print("[*] Pursue from an empty state...")

goal = Goal.with_variables(lambda x, y:
    Goal.both(
        Goal.equal(x, 5),
        Goal.equal(y, 7)))
states = goal.pursue_in(EMPTY_STATE)

print(EMPTY_STATE)
for state in states:
    print(state)            # just print the state since the result is a single state

print('\r\n')


#####
# Nested And-Or conditions
#
print("[*] Problem: Both (a = 7) And (b = 5 Or b = 6).")
print("[*] Pursue from an empty state...")

goal = Goal.with_variables(lambda a, b:
    Goal.both(
        Goal.equal(a, 7),
        Goal.either(
            Goal.equal(b, 5),
            Goal.equal(b, 6))))
states = goal.pursue_in(EMPTY_STATE)

print(EMPTY_STATE)
for state in states:
    print(state)            # This Goal produces two states as results {a => 7, b => 5}, and {a => 7, b => 6}

print('\r\n')


#####
# Contradictions
#
print("[*] Problem: Both x = 1 And x = 2 (a contradiction)")
print("[*] Pursue from an empty state...")

goal = Goal.with_variables(lambda x:
    Goal.both(
        Goal.equal(x, 1),
        Goal.equal(2, x)))
states = goal.pursue_in(EMPTY_STATE)

print(EMPTY_STATE)
for state in states:
    print(state)            # This Goal produces ZERO states

print('\r\n')


#####
# Pairs and Sequences (lists)
#
print("[*] Problem: Pair(x, 3) is equal to Pair(y, Pair(y, 5)).")
print("[*] Pursue from an empty state...")

goal = Goal.with_variables(lambda x, y:
    Goal.equal(
        Pair(3, x),
        Pair(y, Pair(5, y))))
states = goal.pursue_in(EMPTY_STATE)

print(EMPTY_STATE)
for state in filter(None, states):
    print(state)

print('\r\n')


#####
# Appending data to Sequences 01
#
print("[*] Problem: Results of appending the sequence 'he' to the sequence 'llo' and that's equal to x then what is the value of x?")
print("[*] Pursue from an empty state...")

goal = Goal.with_variables(lambda x:
    append(
        Sequence.from_list(['h', 'e']),
        Sequence.from_list(['l', 'l', 'o']),
        x))
states = goal.pursue_in(EMPTY_STATE)

states = filter(None, states)
result = next(states).result()
print(EMPTY_STATE)
print(Sequence.to_list(result))

print('\r\n')


#####
# Appending data to Sequences 02
#
print("[*] Problem: What is x if appending the sequence 'lo' to x produces the sequence 'hello'?")
print("[*] Pursue from an empty state...")

goal = Goal.with_variables(lambda x:
    append(
        x,
        Sequence.from_list(['l', 'o']),
        Sequence.from_list(['h', 'e', 'l', 'l', 'o'])))
states = goal.pursue_in(EMPTY_STATE)

states = filter(None, states)
result = next(states).result()
print(EMPTY_STATE)
print(Sequence.to_list(result))

print('\r\n')


#####
# Reasoning about values of variables from Sequences.
# Reasoning about all possible values of variables.
#
print("[*] Problem: x and y appended gives the sequence 'hello' then what are x and y?")
print("[*] Pursue from an empty state...")

goal = Goal.with_variables(lambda x, y:
    append(
        x,
        y,
        Sequence.from_list(['h', 'e', 'l', 'l', 'o'])))
states = goal.pursue_in(EMPTY_STATE)

print(EMPTY_STATE)
for state in filter(None, states):
    print(list(map(Sequence.to_list, state.results(2))))

print('\r\n')


#####
# Arithmetic: Addition 01
#
print("[*] Problem: If 5 is added to 3 what would be x?")
print("[*] Pursue from an empty state...")

goal = Goal.with_variables(lambda x:
    add(
        peano.to_peano(5),
        peano.to_peano(3),
        x))
states = goal.pursue_in(EMPTY_STATE)

for state in filter(None, states):
    print(peano.from_peano(state.result()))

print('\r\n')


#####
# Arithmetic: Addition 02
#
print("[*] Problem: What is x if added to 3 gives me 8?")
print("[*] Pursue from an empty state...")

goal = Goal.with_variables(lambda x:
    add(
        x,
        peano.to_peano(3),
        peano.to_peano(8)))
states = goal.pursue_in(EMPTY_STATE)

for state in filter(None, states):
    print(peano.from_peano(state.result()))

print('\r\n')


#####
# Arithmetic: Addition 03
#
print("[*] Problem: If x and y added gives 8 what x and y could be?")
print("[*] Pursue from an empty state...")

goal = Goal.with_variables(lambda x, y:
    add(
        x,
        y,
        peano.to_peano(8)))
states = goal.pursue_in(EMPTY_STATE)

for state in filter(None, states):
    print(list(map(peano.from_peano, state.results(2))))

print('\r\n')


#####
# Arithmetic: Multiplication 01
#
print("[*] Problem: If x is the result of 3 multiplied by 8, what is x?")
print("[*] Pursue from an empty state...")

goal = Goal.with_variables(lambda x, y:
    multiply(
        peano.to_peano(3),
        peano.to_peano(8),
        x))
states = goal.pursue_in(EMPTY_STATE)

states = next(filter(None, states))
print(peano.from_peano(states.result()))

print('\r\n')


#####
# Arithmetic: Multiplication 02
#
print("[*] Problem: If x and y multiplied together gives me 24, what could x and y be?")
print("[*] Pursue from an empty state...")

goal = Goal.with_variables(lambda x, y:
    multiply(
        x,
        y,
        peano.to_peano(24)))
states = goal.pursue_in(EMPTY_STATE)

states = itertools.islice(filter(None, states), 8)
for state in states:
    print(list(map(peano.from_peano, state.results(2))))

