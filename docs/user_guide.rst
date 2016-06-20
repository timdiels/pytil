User guide
==========

Depending on Chicken Turtle Util
--------------------------------
Because Chicken Turtle Util (CTU) offers such a wide variety of features, most of its dependencies
are optional so you only need to install the dependencies of the packages you
actually use.  To install all dependencies of the algorithms package for
example, use ``pip install chicken_turtle_util[algorithms]``.
If you are not familiar with pip, see `pip's quickstart guide
<https://pip.pypa.io/en/stable/quickstart/>`_.


Application contexts
--------------------

.. currentmodule:: chicken_turtle_util.application

Every application, regardless of its type of interface, eventually develops an
`Application` or `ApplicationContext` class to store its application-global
(not actually global!) objects. For example, you may need to share database
access across your application using a `Database` object, or make a
configuration available application-wide. This is what :class:`Context` is for.
Such a class is instantiated at the start of the application and is passed
around through all objects specific to the application.

Not every application context is the same though, so
:mod:`chicken_turtle_util.application` provides you with the building blocks,
called `mixins`_, to build your own. For example :class:`DatabaseMixin` add
`context.database` to `Context`, and :class:`ConfigurationMixin` adds
`context.configuration`. You can do this as follows::

    from my_application import Database, Configuration
    from chicken_turtle_util import application as app
    DatabaseMixin = app.DatabaseMixin(Database)
    ConfigurationMixin = app.ConfigurationMixin(Configuration, 'Config X: /example/location/app_specific_path.conf')
    class MyApplicationContext(DatabaseMixin, ConfigurationMixin, Context):
        pass

Instances of `MyApplicationContext` will then have a `database` and
`configuration` attribute.

.. warning::

    In the list of base classes, note that `Context` must be last and if a
    mixin `M1` derives from another mixin `M2`, it should appear to the left of
    `M2` (or simply remove `M2` from the list). You likely won't have to think
    about this as you are unlikely to include `M2` when already deriving from
    `M1`.

    But if you do get it wrong::
    
        class Mixin2(Context):
            pass

        class Mixin1(Mixin2, Context):
            pass

        class MyApplicationContext(Mixin2, Mixin1):
            pass

    then Python will greet you with::

        TypeError: Cannot create a consistent method resolution
        order (MRO) for bases Mixin2, Mixin1

    which can be fixed with::

        class MyApplicationContext(Mixin1):
            pass

    or::

        class MyApplicationContext(Mixin1, Mixin2):
            pass

As any application is started via a command line interface (i.e. your
executable is called with a list of arguments), :class:`Context` provides
a `command` attribute that you can use like so::

    @Context.command()
    def main(context):
        pass

This turns `main` into a `click`_ Command. If you are not familiar with
`click`_, go check it out. You can add options to it just as you would with any
other `click` command::

    import click

    @click.option('--configuration-file')
    @Context.command()
    def main(configuration_file, context)
        pass

Most mixins add command line options to the command and `@Context.command`
ensures the arguments parsed by `click`_ are passed to the mixins.  For
example, `ConfigurationMixin` adds a `--configuration` option.  Any left over
arguments, as well as the resulting Context instance, are passed to the
decorated function; `configuration_file` is passed to `main` in this example.

Now, for a complete example::

    # main.py
    import click
    from chicken_turtle_util import application as app

    # version of your application, BasicsMixin uses it in its --version option
    __version__ = '1.0.0'

    class Context(app.BasicsMixin(__version__), app.Context):

        # You don't have to put everything in mixins, you can also add it
        # directly
        @property
        def times(self):
            return 3

    @click.argument('message')
    @Context.command()
    def main(message, context):
        '''
        Amazing application that repeats your message
        '''
        print(message * context.times)

    # If you package your application using setup.py (setuptools),
    # use setup(..., entry_points={ 'console_scripts': [ 'myapp': # 'myapp_package.main:main']})
    # instead of calling main directly as follows. Once installed, it can be called as `myapp`.
    if __name__ == '__main__':
        main()

This can then be used as::

    $ python main.py --help
    Usage: main.py [OPTIONS] MESSAGE

      Amazing application that repeats your message

    Options:
      --version   Show the version and exit.
      -h, --help  Show this message and exit.
    $ python main.py 'Hi there. '
    Hi there. Hi there. Hi there. 
    $ python main.py --version   
    main.py, version 1.0.0

For information on how to create your own mixins, see :class:`Context`.

..
  Configuration files
  -------------------

.. _mixins: https://en.wikipedia.org/wiki/Mixin
.. _click: http://click.pocoo.org/6/
