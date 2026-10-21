---
Title: Python's functools.partial
Date: 2026-10-21 07:00
Category: Computer Science
Tags: cs, python, functools, functional-programming, tech-notes
Slug: functools-partial
Status: published
---

**`functools.partial` creates a callable with some arguments already supplied.** This is called *partial application*: specialize an existing function, then provide the remaining arguments later. Creating the partial does not execute the original function. [Python's functional programming HOWTO](https://docs.python.org/3/howto/functional.html#the-functools-module)

## Pre-fill an argument

Suppose a function raises a number to a power. We can make a reusable version that defaults to squaring:

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)

print(square(5))              # 25
print(square(3))              # 9
print(square(5, exponent=3))  # 125
```

`square(5)` calls `power(5, exponent=2)`. Stored keyword arguments can be overridden when calling the partial, so the last call uses exponent `3`. The original `power` function remains unchanged. [partial documentation](https://docs.python.org/3/library/functools.html#functools.partial)

## Argument order matters

Without placeholders, stored positional arguments come first; new positional arguments follow them:

```python
two_to_power = partial(power, 2)
print(two_to_power(5))  # 32: power(2, 5)
```

This fixes the **base**, whereas `partial(power, exponent=2)` supplies the **exponent**. Also, `square(5, 3)` raises `TypeError`: it supplies `exponent` both positionally and through the stored keyword. Override it by name instead.

## Where it helps

Use `partial` when an API expects a callable but you want to configure some inputs beforehand: callbacks, reusable settings, or functions passed to `map`. Here, `map` supplies each base while `square` supplies the exponent:

```python
print(list(map(square, [2, 3, 4])))  # [4, 9, 16]
```

A lambda such as `lambda base: power(base, 2)` expresses the same calculation. As a practical rule, use `partial` for argument binding and a regular `def` when the wrapper needs validation or additional logic. See the [HOWTO's discussion of small functions](https://docs.python.org/3/howto/functional.html#small-functions-and-the-lambda-expression).

## Leaving positional gaps: Python 3.14+

[`Placeholder`](https://docs.python.org/3/library/functools.html#functools.Placeholder) reserves a positional slot for a later argument. This lets us bind the second position while leaving the first open:

```python
from functools import Placeholder

cube = partial(power, Placeholder, 3)
print(cube(4))  # 64: power(4, 3)
```

Every placeholder must receive a positional argument when the partial is called. The earlier examples also work on Python versions before 3.14.
