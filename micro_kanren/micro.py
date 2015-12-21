from itertools import islice, chain
from inspect import signature
import micro_kanren.utils as utils
import micro_kanren.peano as peano
from micro_kanren.sequence import Pair, Sequence


#####
# DEFINE VARIABLE
#
class Variable:
    '''
    The Variable data structure.
    Represents variables in States, and only holds a variable name to refer to variables.
    '''
    def __init__(self, name):
        self.name = name

    def inspect(self):
        return str(self)

    def __str__(self):
        return "#<Var: {}>".format(self.name)


#####
# DEFINE STATE
#
class State:
    '''
    The State data structure.
    Holds a list of variables and a dictionary for mapping variables to values, this is an immutable data structure.
    '''
    def __init__(self, variables=[], values=dict()):
        self._variables, self._values = variables, values

    @property
    def variables(self):
        return self._variables

    @property
    def values(self):
        return self._values

    def create_variables(self, names):
        new_variables = list(map(Variable, names))
        return (State(self.variables + new_variables, self.values), new_variables)

    def assign_values(self, new_values):
        return State(self.variables.copy(), {**self.values, **new_values})

    def final_value_of(self, key):
        if key in self.values:
            return self.final_value_of(self.values[key])
        elif isinstance(key, Variable):
            return self.final_value_of(key.name)
        elif isinstance(key, Pair):
            return Pair(self.final_value_of(key.left), self.final_value_of(key.right))
        else:
            return key

    def value_of(self, key):
        if key in self.values.keys():
            return self.value_of(self.values[key])
        elif isinstance(key, Pair):
            pair = Pair(
                self.value_of(key.left),
                self.value_of(key.right)
            )
            return pair
        else:
            return key

    def unify(self, a, b):
        a, b = self.value_of(a), self.value_of(b)

        if a == b:
            return self
        elif isinstance(a, Variable):
            return self.assign_values({a: b})
        elif isinstance(b, Variable):
            return self.assign_values({b: a})
        elif isinstance(a, Pair) and isinstance(b, Pair):
            state = self.unify(a.left, b.left)
            return state.unify(a.right, b.right) if state else state

    def results(self, n):
        return [self.value_of(result) for result in islice(self.variables, n)]

    def result(self):
        return self.results(1)[0]

    def __str__(self):
        return "#<State: @id={}, @variables={}, @values={}>".format(id(self), [str(var) for var in self.variables], {str(key):str(val) for key, val in self.values.items()})


#####
# DEFINE GOAL
#
class Goal:
    '''The Goal data structure. Holds lambda functions for executing conditions on states.'''
    def __init__(self, function):
        self.function = function

    def pursue_in(self, state):
        return self.function(state)

    def pursue_in_each(self, states):
        results = self.pursue_in(next(states))
        results = utils.interleave(chain.from_iterable([results, self.pursue_in_each(states)]))
        for state in results:
            yield state

    @staticmethod
    def with_variables(binding_function):
        # get function signature and then get the names of its parameters (free variables)
        names = list(signature(binding_function).parameters.keys())
        def function(state):
            if not state:
                return None
            state, variables = state.create_variables(names)
            goal = binding_function(*variables)
            return goal.pursue_in(state)
        return Goal(function)

    @staticmethod
    def equal(a, b):
        def function(state):
            if not state:
                return None
            state = state.unify(a, b)
            return iter([state]) if state else None
        return Goal(function)

    @staticmethod
    def either(first_goal, second_goal):
        def function(state):
            first_stream = first_goal.pursue_in(state)
            second_stream = second_goal.pursue_in(state)
            return utils.interleave(first_stream, second_stream)
        return Goal(function)

    @staticmethod
    def both(first_goal, second_goal):
        def function(state):
            states = first_goal.pursue_in(state)
            return second_goal.pursue_in_each(states)
        return Goal(function)



#####
# DEFINE RELATIONS
#
def append(a, b, c):
    return Goal.either(
        Goal.both(
            Goal.equal(a, Sequence.EMPTY),
            Goal.equal(b, c)
        ),
        Goal.with_variables(lambda first, rest_of_a, rest_of_c:
            Goal.both(
                Goal.both(
                    Goal.equal(a, Pair(first, rest_of_a)),
                    Goal.equal(c, Pair(first, rest_of_c))
                ),
                append(rest_of_a, b, rest_of_c)
            )
        )
    )


def add(x, y, z):
    return Goal.either(
        Goal.both(
            Goal.equal(x, peano.ZERO),
            Goal.equal(y, z)
        ),
        Goal.with_variables(lambda smaller_x, smaller_z:
            Goal.both(
                Goal.both(
                    Goal.equal(x, Pair(peano.SUCCESSOR, smaller_x)),
                    Goal.equal(z, Pair(peano.SUCCESSOR, smaller_z))
                ),
                add(smaller_x, y, smaller_z)
            )
        )
    )


def multiply(x, y, z):
    return Goal.either(
        Goal.both(
            Goal.equal(x, peano.ZERO),
            Goal.equal(z, peano.ZERO)
        ),
        Goal.with_variables(lambda smaller_x, smaller_z:
            Goal.both(
                Goal.both(
                    Goal.equal(x, Pair(peano.SUCCESSOR, smaller_x)),
                    add(smaller_z, y, z)
                ),
                multiply(smaller_x, y, smaller_z)
            )
        )
    )

