Developer documentation
=======================
Documentation for developers/contributors of pytil.

The project follows a `simple project`_ structure and associated workflow. Please
read `its documentation <simple project_>`_.

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

.. _simple project: http://python-project.readthedocs.io/en/1.1.1/simple.html
