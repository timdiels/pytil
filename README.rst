Chicken Turtle Util (CTU) provides an API of various Python utility functions.

Chicken Turtle Util is alpha. None of the interface is stable (yet), meaning it
may change in the future.

Chicken Turtle Util offers a variety of features, as such we kept most
dependencies optional.  When using a module, add/install its dependencies,
listed in its corresponding ``*_requirements.in`` file found in the root of the
project; e.g.  `cli_requirements.in`__ lists the dependencies of
`chicken_turtle_util.cli`.

.. __: https://github.com/timdiels/chicken_turtle_util/blob/master/cli_requirements.in


Features
========

- `algorithms.spread_points_in_hypercube`:

  Place `n` points in a unit hypercube such that the minimum distance between
  points is approximately maximal

- `algorithms.multi_way_partitioning`: Greedily divide weighted items equally across bins (multi-way partition problem)       
- `data_frame` and `series`: `pandas <http://pandas.pydata.org/>`_ utility functions

  - `data_frame.replace_na_with_none`: Replace `NaN` values in `DataFrame` with `None`
  - `data_frame.split_array_like`: Split cells with `array_like` values along row axis.
  - `series.invert`: Swap index with values of series

- `dict`: dictionary utilities:

  - `invert`: Invert dict by swapping each value with its key
  - `DefaultDict`: Like `collections.defaultdict`, but its value factory function takes a key argument, e.g. ``DefaultDict(lambda key: MyClass(key))``
  - `pretty_print_head`: Pretty print the 'first' lines of a dict

- `function.compose`: Compose functions
- `http.download`: Download http resource (using `requests`) and save to file name suggested by HTTP server
- `iterable.sliding_window`: Iterate using a sliding window
- `iterable.partition`: Split iterable into partitions
- `iterable.is_sorted`: Get whether iterable is sorted ascendingly
- `iterable.flatten`: Flatten shallowly zero or more times
- `set.merge_by_overlap`: Of a list of sets, merge those that overlap, in place
- `logging.set_level`: Context manager to temporarily change log level of logger
- `cli`: extensions to `click <http://click.pocoo.org/>`_ for building CLI applications
- `pyqt.block_signals`: Context manager to temporarily turn on `QObject.blockSignals`
- `sqlalchemy.log_sql`: Context manager to temporarily log sql statements emitted by `sqlalchemy <http://www.sqlalchemy.org/>`_
- `various.Object`: Like `object`, but does not raise given args to `__init__`

Links
=====
- `Documentation <http://pythonhosted.org/chicken_turtle_util/>`_
- `PyPI <https://pypi.python.org/pypi/chicken_turtle_util/>`_
- `GitHub <https://github.com/timdiels/chicken_turtle_util/>`_

Changelist
==========

.. todo: add to overview

v2.1.0 (to be released)
-----------------------
- Added cli.ConfigurationMixin: application context mixin for loading a configuration
- Added configuration.ConfigurationLoader: loads a single configuration from one or more files
- cli.Context: `cli_options()` replaced by `command()`, which is more flexible
- Removed cli.command. Use cli.Context.command() instead
- Added `path.write`: create or overwrite file with contents
- Added `path.read`: get file contents
- Added `test.temp_dir_cwd`: pytest fixture that sets current working directory to a temporary directory
- Added `dict.assign`: assign one dict to the other through mutations

v2.0.4
------
No changelist

Developer guide
===============

Docstrings type language
------------------------

Docstrings must follow `NumPy style <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt#sections>`_

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
(duck typing) is allowed. None is not allowed. ::

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

Project decisions
-----------------

API design
~~~~~~~~~~

If it's a path, expect a `pathlib.Path`, not a `str`.

If extending a module from another project, e.g. `pandas`, use the same name
as the module. While a ``from pandas import *`` would allow the user to access
functions of the real pandas module through the extended module, we have no
control over additions to the real pandas, which could lead to name clashes
later on, so don't.

Decorators and context managers should not be provided directly but should be
returned by a function. This avoids confusion over whether or not parentheses
should be used ``@f`` vs ``@f()``, and parameters can easily be added in the
future.

If a module is a collection of instances of something, give it a plural name,
else make it singular. E.g. `exceptions` for a collection of `Exception`
classes, but `function` for a set of related functions operating on functions.

API implementation
~~~~~~~~~~~~~~~~~~

Do not prefix imports with underscore. When importing things, they also are
exported, but `help` or Sphinx documentation will not include them and thus a
user should realise they should not be used. E.g.  ``import numpy as np`` in
`module.py` can be accessed with `module.np`, but it isn't mentioned in
`help(module)` or Sphinx documentation.
