API reference
=============

See modules for a short description of each modules. For a full listing of the
contents of all modules, see the module contents overview.

The API reference makes heavy use of a `type language`_; for
example, to describe exactly what arguments can
be passed to a function.  

.. _type language: type_language.html

Modules
-------
    
.. currentmodule:: pytil
.. autosummary::
    :toctree: api

    algorithms
    asyncio
    click
    configuration
    data_frame
    debug
    dict
    difflib
    exceptions
    function
    hashlib
    http
    inspect
    iterable
    logging
    multi_dict
    observable
    path
    pymysql
    series
    set
    sqlalchemy
    test
   

Module contents overview
------------------------

.. rubric:: algorithms
.. currentmodule:: pytil.algorithms
.. autosummary::
    :nosignatures:
    
    multi_way_partitioning
    spread_points_in_hypercube
    toset_from_tosets
    
.. rubric:: asyncio
.. currentmodule:: pytil.asyncio
.. autosummary::
    :nosignatures:
    
    stubborn_gather
    
.. rubric:: click
.. currentmodule:: pytil.click
.. autosummary::
    :nosignatures:
    
    argument
    assert_runs
    option
    password_option
    
.. rubric:: configuration
.. currentmodule:: pytil.configuration
.. autosummary::
    :nosignatures:
    
    ConfigurationLoader
    
.. rubric:: data_frame
.. currentmodule:: pytil.data_frame
.. autosummary::
    :nosignatures:
    
    assert_equals
    equals
    replace_na_with_none
    split_array_like
    
.. rubric:: debug
.. currentmodule:: pytil.debug
.. autosummary::
    :nosignatures:
    
    pretty_memory_info
    
.. rubric:: dict
.. currentmodule:: pytil.dict
.. autosummary::
    :nosignatures:
    
    pretty_print_head
    DefaultDict
    invert
    assign

.. rubric:: difflib
.. currentmodule:: pytil.difflib
.. autosummary::
    :nosignatures:
    
    line_diff

.. rubric:: exceptions
.. currentmodule:: pytil.exceptions
.. autosummary::
    :nosignatures:
    
    exc_info
    UserException
    InvalidOperationError
    
.. rubric:: function
.. currentmodule:: pytil.function
.. autosummary::
    :nosignatures:
    
    compose

.. rubric:: hashlib
.. currentmodule:: pytil.hashlib
.. autosummary::
    :nosignatures:
    
    base85_digest
    
.. rubric:: http
.. currentmodule:: pytil.http
.. autosummary::
    :nosignatures:
    
    download

.. rubric:: inspect
.. currentmodule:: pytil.inspect
.. autosummary::
    :nosignatures:
    
    call_args
    
.. rubric:: iterable
.. currentmodule:: pytil.iterable
.. autosummary::
    :nosignatures:
    
    sliding_window
    partition
    is_sorted
    flatten
    
.. rubric:: logging
.. currentmodule:: pytil.logging
.. autosummary::
    :nosignatures:
    
    configure
    set_level
    
.. rubric:: multi_dict
.. currentmodule:: pytil.multi_dict
.. autosummary::
    :nosignatures:
    
    MultiDict
    
.. rubric:: observable
.. currentmodule:: pytil.observable
.. autosummary::
    :nosignatures:
    
    Set
    
.. rubric:: path
.. currentmodule:: pytil.path
.. autosummary::
    :nosignatures:
    
    assert_equals
    assert_mode
    chmod
    hash
    read
    remove
    sorted_lines
    write
    
.. rubric:: pymysql
.. currentmodule:: pytil.pymysql
.. autosummary::
    :nosignatures:
    
    patch

.. rubric:: series
.. currentmodule:: pytil.series
.. autosummary::
    :nosignatures:
    
    assert_equals
    equals
    invert
    split
    
.. rubric:: set
.. currentmodule:: pytil.set
.. autosummary::
    :nosignatures:
    
    merge_by_overlap
    
.. rubric:: sqlalchemy
.. currentmodule:: pytil.sqlalchemy
.. autosummary::
    :nosignatures:
    
    log_sql
    pretty_sql
    
.. rubric:: test
.. currentmodule:: pytil.test
.. autosummary::
    :nosignatures:
    
    assert_text_contains
    assert_text_equals
    assert_lines_equal
    assert_matches
    assert_search_matches
    reset_loggers
    temp_dir_cwd
