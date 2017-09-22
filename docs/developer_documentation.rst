Developer documentation
=======================
Documentation for developers/contributors of pytil.

The project follows a `simple project`_ structure and associated workflow. Please
read `its documentation <simple project_>`_.

Project decisions
-----------------

API design
~~~~~~~~~~
If it's a path, expect a :py:class:`~pathlib.Path`, not a `str`.

If extending a module from another project, e.g. `pandas`, use the same name
as the module.

If a module is a collection of instances of something, give it a plural name,
else make it singular. E.g. ``exceptions`` for a collection of ``Exception``
classes, but ``function`` for a set of related functions operating on functions.

API implementation
~~~~~~~~~~~~~~~~~~
When importing things, they also are exported, we do not attempt to remedy this.
E.g. ``import numpy as np`` in ``module.py`` can be accessed with ``module.np``,
but `help` or Sphinx documentation will not include them. We assume a user will
not use anything not mentioned in the documentation.

.. _simple project: http://python-project.readthedocs.io/en/1.1.1/simple.html
