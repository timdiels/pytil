Developer documentation
=======================

Documentation for developers/contributors of Chicken Turtle Util.

Coding guidelines
-----------------

- Docstrings must follow 
  `NumPy style <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt#sections>`_.
- Use the `type language <type_language>`_ when referring to a type, e.g. in
  the Parameters section.
- When using someone else's code or idea, give credit in a comment in the
  source file, not in the documentation.
  
Commit checklist
----------------

Do not forget any of these steps before committing:

- Tests adjusted to match what you changed (preferably test-driven)
- API has docstrings and guidelines are followed
- docs/api_reference.rst updated
- docs/api/... updated

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
