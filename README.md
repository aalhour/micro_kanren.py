# μKanren.py

μKanren (MuKanren), which is also known as [microKanren](papers/Hemann_MuKanren_2013.pdf), is a declarative-relational programming language, that was originally presented in the book [The Reasoned Schemer](http://www.amazon.com/dp/0262562146). In microKanren You would solve a problem by declaring it as an end goal Goal that consists of relations between variables and states, and then you let microKanren handle how to solve it.

This is a Python 3 port of [Tom Stuart's μKanren](https://github.com/tomstuart/kanren) implementation in Ruby.


## Motivation:

Tom Stuart talked very concisely about this paradigm in his talk [Hello, Declarative World!](https://skillsmatter.com/skillscasts/6523-hello-declarative-world) and its accompanying [article](http://codon.com/hello-declarative-world).

If you find it difficult to play around with this library, then I urge you to watch Tom's video as it builds up a set of interesting ideas from simple constructs. If you're feeling adventurous, then head over to **examples/**, and try to build on them.

Differences to Tom's Ruby project:
  * The List data structure is renamed to Sequence, since Python has a list data structure already (Ruby has arrays).
  * The Ruby blocks are implemented as Python lambda functions.
  * Enumerators are implemented as normal named functions which **yield** values (generators/iterators).
  * State, Variable, Goal and Relations are all incapsulated in the [micro](micro_kanren/micro.py) module.
  * Pair and Sequence are implemented in the [sequence](micro_kanren/sequence.py) module.

All the examples from the talk can be found under the **examples/** directory.


## Example:

Suppose I have two variables: **x**, and **y**. If **x** and **y** multiplied gives me **24**, what could x and y be?

**Program:**

```python
empty_state = State()
goal = Goal.with_variables(lambda x, y:
    multiply(
        x,
        y,
        peano.to_peano(24)))                               # encode 24 in peano's arithmetics
states = goal.pursue_in(empty_state)

states = itertools.islice(filter(None, states), 8)         # take 8 states only

# Print the results
for state in states:
    print(list(map(peano.from_peano, state.results(2))))   # map x and y from peano to decimal
```

**Output:**

```bash
[1, 24]
[2, 12]
[3, 8]
[4, 6]
[6, 4]
[8, 3]
[12, 2]
[24, 1]
```

Numbers in this microKanren implementation are encoded using Peano's arithmetic (see: [peano module](μKanren/peano.py)) when supplied to Goals and then decoded when returned as outputs.


## Notes:

This project was developed on OSX 10 and using Python 3.5.1, I haven't debugged it on other platforms. This is for educational purposes only. If you find any bugs or other problems with the code or even would like to contribute, please open an issue.

Happy coding!

