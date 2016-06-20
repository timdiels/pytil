Python type language
======================

When documenting code, it is often necessary to refer to the type of an
argument or a return.  Here, I introduce a language for doing so in a
semi-formal manner.

First off, I define these pseudo-types:

- iterable: something you can iterate over once (or more) using `iter`
- iterator: something you can call `next` on
- collection: something you can iterate over multiple times

I define the rest of the type language through examples::

    pathlib.Path

Expects a `pathlib.Path`-like, i.e. anything that looks like a `pathlib.Path`
(`duck typing <http://stackoverflow.com/a/4205163/1031434>`_) is allowed. None is not allowed. ::

    exact(pathlib.Path)

Expects a `Path` or derived class instance, so no duck typing (and no None). ::

    pathlib.Path or None

Expect a `pathlib.Path`-like or None. When None is allowed it must be
explicitly specified like this. ::

    bool or int

Expect a boolean or an int. ::

    {bool}

A set of booleans. ::

    {any}

A set of anything. ::

    {'apples' => bool, 'name' => str}

A dictionary with keys 'apples' and 'name' which respectively have a boolean
and a string as value. (Note that the ``:`` token is already used by Sphinx, and
``->`` is usually used for lambdas, so we use ``=>`` instead). ::

    dict(apples=bool, name=str)

Equivalent to the previous example. ::

    Parameters
    ----------
    field : str
    dict_ : {field => bool}

A dictionary with one key, specified by the value of `field`, another parameter (but can be any expression, e.g. a global). ::

    {apples => bool, name => str}

Not equivalent to the apples dict earlier. `apples` and `name` are references to the value used as a key. ::

    (bool,)

Tuple of a single bool. ::

    [bool]

List of 0 or more booleans. ::

    [(bool, bool)]

List of tuples of boolean pairs. ::

    [(first :: bool, second :: bool)]

Equivalent type compared to the previous example, but you can more easily refer
to the first and second bool in your parameter description this way. ::

    {item :: int}

Set of int. We can refer to the set elements as `item`. ::

    iterable(bool)

Iterable of bool. Something you can call `iter` on. ::

    iterator(bool)

Iterator of bool. Something you can call `next` on. ::

    type_of(expression)

Type of expression, avoid when possible in order to be as specific as
possible. ::

    Parameters
    ----------
    a : SomeType
    b : type_of(a.nodes[0].key_function)

`b` has the type of the retrieved function. ::

    (int, str, k=int) -> bool

Function that takes an int and a str as positional args, an int as keyword arg
named 'k' and returns a bool. ::

    func :: int -> bool

Function that takes an int and returns a bool. We can refer to it as `func`.
