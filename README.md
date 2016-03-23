Chicken Turtle Util (CTU) provides an API of various Python utility functions.

Chicken Turtle Util is pre-alpha. None of the interface is stable, meaning it may
change in the future.

Chicken Turtle Util has some optional dependencies. E.g. to use
`chicken_turtle.pyqt`, you will need to add PyQt to your project's
dependencies. For now, you'll have to let the `ImportError`s guide you to the
right dependencies to add to setup.py assuming your tests have full coverage.

## Developer guide

### Docstrings type language

Docstrings must follow [NumPy style](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt#sections)

When using someone else's code or idea, give credit in a comment in the
source file, not in the documentation.

When describing a type (e.g. in the Parameters section), do so in the type
language described below.

You can use these pseudo-types:

- iterable: something you can iterate over once (or more) using `iter`
- iterator: something you can call `next` on
- collection: something you can iterate over multiple times

The rest of the type language is described by example::

    pathlib.Path

Expects a `pathlib.Path`-like, i.e. anything that looks like a `pathlib.Path`
(duck typing) is allowed. None is not allowed.

    exact(pathlib.Path)

Expects a `Path` or derived class instance, so no duck typing (and no None).

    pathlib.Path or None

Expect a `pathlib.Path`-like or None. When None is allowed it must be
explicitly specified like this.

    bool or int

Expect a boolean or an int.

    {bool}

A set of booleans.

    {any}

A set of anything.

    {'apples': bool, 'name': str}

A dictionary with keys 'apples' and 'name' which respectively have a boolean
and a string as value.

    dict(apples=bool, name=str)

Equivalent to the previous example.

    Parameters
    ----------
    field : str
    dict_ : {field: bool}

A dictionary with one key, specified by the value of `field`, another parameter (but can be any expression, e.g. a global).

    (bool,)

Tuple of a single bool.

    [bool]

List of 0 or more booleans.

    [(bool, bool)]

List of tuples of boolean pairs.

    [(first :: bool, second :: bool)]

Equivalent type compared to the previous example, but you can more easily refer
to the first and second bool in your parameter description this way.

    {item :: int}

Set of int. We can refer to the set elements as `item`.

    iterable(bool)

Iterable of bool. Something you can call `iter` on.

    iterator(bool)

Iterator of bool. Something you can call `next` on.

    type_of(expression)

Type of expression, avoid when possible in order to be as specific as possible.

    Parameters
    ----------
    a : SomeType
    b : type_of(a.nodes[0].key_function)

`b` has the type of the retrieved function.

    (int, str, k=int) -> bool

Function that takes an int and a str as positional args, an int as keyword arg
named 'k' and returns a bool.

    func :: int -> bool

Function that takes an int and returns a bool. We can refer to it as `func`.

### Project decisions

#### API design

If it's a path, expect a `pathlib.Path`, not a `str`.

If extending a module from another project, e.g. `pandas`, use the same name
as the module. While a `from pandas import *` would allow the user to access
functions of the real pandas module through the extended module, we have no
control over additions to the real pandas, which could lead to name clashes
later on, so don't.

Decorators and context managers should not be provided directly but should be
returned by a function. This avoids confusion over whether or not parentheses
should be used `@f` vs `@f()`, and parameters can easily be added in the
future.

If a module is a collection of instances of something, give it a plural name,
else make it singular. E.g. `exceptions` for a collection of `Exception`
classes, but `function` for a set of related functions operating on functions.

#### API implementation

Do not prefix imports with underscore. When importing things, they also are
exported, but `help` or Sphinx documentation will not include them and thus a
user should realise they should not be used. E.g.  `import numpy as np` in
`module.py` can be accessed with `module.np`, but it isn't mentioned in
`help(module)` or Sphinx documentation.
