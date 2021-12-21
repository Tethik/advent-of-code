# advent-of-code-2021

My solutions for Advent of Code 2021

## TODO / Ideas

- [] fetch input automagically
- [] automate testing with https://github.com/bats-core/bats-core
- [] utility functions (logging, but also common problems like checking diagonals etc)

## Cool features discovered

Here are some of the python features I've discovered while working on the challenges and comparing with friends/colleagues.

- **collections.Counter** is useful across many challenges that requires counting and merging counts.

- The **set** data structure has handy functions to simply compute intersections and unions via operators: `union = a | b`, `intersect = a & b`

- The [**statistics**](https://docs.python.org/3/library/statistics.html) module has some useful functions, like **mean** and **median**. Likely other useful functions too. Didn't know this module existed.

- **itertools.chain()** and **chain.from_iterable()** are both super useful when dealing with nested lists.

- **itertools.enumerate()**,**itertools.product()**, and **itertools.combinations()** are all super useful functions when
  dealing with combinatorics.

- **math.prod()** computes the product of the args, similar to sum but when you need multiplication instead.

- **functools.lru_cache(None)** allows for super easy memoization.
