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
    
.. currentmodule:: chicken_turtle_util
.. autosummary::
    :toctree: api

    algorithms
    cli
    configuration
    data_frame
    debug
    dict
    exceptions
    function
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
.. currentmodule:: chicken_turtle_util.algorithms
.. autosummary::
    :nosignatures:
    
    multi_way_partitioning
    spread_points_in_hypercube
    toset_from_tosets
    
.. rubric:: cli
.. currentmodule:: chicken_turtle_util.cli
.. autosummary::
    :nosignatures:
    
    option
    argument
    password_option
    
.. rubric:: configuration
.. currentmodule:: chicken_turtle_util.configuration
.. autosummary::
    :nosignatures:
    
    ConfigurationLoader
    
.. rubric:: data_frame
.. currentmodule:: chicken_turtle_util.data_frame
.. autosummary::
    :nosignatures:
    
    assert_equals
    equals
    replace_na_with_none
    split_array_like
    
.. rubric:: debug
.. currentmodule:: chicken_turtle_util.debug
.. autosummary::
    :nosignatures:
    
    pretty_memory_info
    
.. rubric:: dict
.. currentmodule:: chicken_turtle_util.dict
.. autosummary::
    :nosignatures:
    
    pretty_print_head
    DefaultDict
    invert
    assign
    
.. rubric:: exceptions
.. currentmodule:: chicken_turtle_util.exceptions
.. autosummary::
    :nosignatures:
    
    UserException
    InvalidOperationError
    
.. rubric:: function
.. currentmodule:: chicken_turtle_util.function
.. autosummary::
    :nosignatures:
    
    compose
    
.. rubric:: http
.. currentmodule:: chicken_turtle_util.http
.. autosummary::
    :nosignatures:
    
    download

.. rubric:: inspect
.. currentmodule:: chicken_turtle_util.inspect
.. autosummary::
    :nosignatures:
    
    call_args
    
.. rubric:: iterable
.. currentmodule:: chicken_turtle_util.iterable
.. autosummary::
    :nosignatures:
    
    sliding_window
    partition
    is_sorted
    flatten
    
.. rubric:: logging
.. currentmodule:: chicken_turtle_util.logging
.. autosummary::
    :nosignatures:
    
    set_level
    
.. rubric:: multi_dict
.. currentmodule:: chicken_turtle_util.multi_dict
.. autosummary::
    :nosignatures:
    
    MultiDict
    
.. rubric:: observable
.. currentmodule:: chicken_turtle_util.observable
.. autosummary::
    :nosignatures:
    
    Set
    
.. rubric:: path
.. currentmodule:: chicken_turtle_util.path
.. autosummary::
    :nosignatures:
    
    chmod
    digest
    read
    remove
    write
    
.. rubric:: pymysql
.. currentmodule:: chicken_turtle_util.pymysql
.. autosummary::
    :nosignatures:
    
    patch

.. rubric:: series
.. currentmodule:: chicken_turtle_util.series
.. autosummary::
    :nosignatures:
    
    assert_equals
    equals
    invert
    split
    
.. rubric:: set
.. currentmodule:: chicken_turtle_util.set
.. autosummary::
    :nosignatures:
    
    merge_by_overlap
    
.. rubric:: sqlalchemy
.. currentmodule:: chicken_turtle_util.sqlalchemy
.. autosummary::
    :nosignatures:
    
    log_sql
    pretty_sql
    
.. rubric:: test
.. currentmodule:: chicken_turtle_util.test
.. autosummary::
    :nosignatures:
    
    temp_dir_cwd
