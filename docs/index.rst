Welcome to pytil's documentation!
================================================================================================
pytil (formerly known as `Chicken Turtle Util`_) is a Python utility library.

The `API reference`_ starts with an overview of all the features and then gets
down to the nitty gritty details of each of them. Most of the reference
provides examples.  For a full overview of features see the `module contents
overview`_ of the API reference and the table of contents of the user guide (in
the sidebar) as they are complementary.

The API reference makes heavy use of a `type language`_; for
example, to describe exactly what arguments can
be passed to a function.  

Dependencies are grouped by module. For example, when using
``pytil.data_frame``, you should ``pip install 'pytil[data_frame]'``. To
install dependencies of all modules, use ``pip install 'pytil[all]'``.  If you
are not familiar with pip,
see `pip's quickstart guide <https://pip.pypa.io/en/stable/quickstart/>`_.

While all features are documented and tested, the API is changed frequently.
When doing so, the `major version <semver_>`_ is bumped and a changelog is kept
to help upgrade. Fixes will not be backported. It is recommended to pin the
major version in your setup.py, e.g. for 2.x.y::

    install_requires = ['pytil.*', ...]

Contents:

.. toctree::
   :maxdepth: 2

   api_reference
   type_language
   developer_documentation
   changelog


Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _API reference: api_reference.html
.. _user guide: user_guide.html
.. _module contents overview: api_reference.html#module-contents-overview
.. _type language: type_language.html
.. _semver: http://semver.org/spec/v2.0.0.html
.. _chicken turtle util: http://chicken-turtle-util.readthedocs.io/en/latest/

