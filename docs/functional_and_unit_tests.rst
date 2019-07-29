*************************
Functional and Unit Tests
*************************

Django supports two different test approaches: Doctests and unit tests. We will
look at the advantages and disadvantages of both in this chapter.

Doctests
========

`Doctests <http://docs.python.org/library/doctest.html>`_ are supported by
Django, but they are :djangodocs:`not automatically discovered <releases/1.6/#new-test-runner>`.
In addition the disadvantages outweigh the advantages when you want to write
doctests for Django.

Advantages
----------

* Easy to create
* Augment the code documentation
* Tests are where the source code is

Disadvantages
-------------

* Documentation may be too large (can be bypassed by moving them to the test suite)
* Output of the test execution is not always clear
* Dependencies on the environment (eg interpreter output)
* Database operations are not encapsulated in transactions
* Unicode problems

Therefore we won't write any doctests.

Unit tests
==========

Django uses the Python standard library module
`unittest <http://docs.python.org/library/unittest.html>`_ for
`unit tests <https://en.wikipedia.org/wiki/Unit_testing>`_.

Before we can write the first tests we have to install an additional package:

::

    $ pip install freezegun

The file :file:`recipes/tests.py` currently contains only an import of the ``TestCase`` base class:

.. literalinclude:: ../src/cookbook/recipes/tests.py

It extends ``unittest.TestCase`` and provides additional functionality:

* Automatic :djangodocs:`loading of fixtures <topics/testing/tools/#fixture-loading>`
* Wraps each test in a :djangodocs:`transaction <topics/testing/tools/#transactiontestcase>`
* Creates a :djangodocs:`TestClient <topics/testing/tools/#the-test-client>` instance
* :djangodocs:`Django-specific assertions <topics/testing/tools/#assertions>` for testing for things like redirection and form errors

Add the following code:

.. literalinclude:: ../src/cookbook_tests/recipes/tests.py

And run the tests:

::

    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    .ss.
    ----------------------------------------------------------------------
    Ran 4 tests in 0.580s

    OK (skipped=2)
    Destroying test database for alias 'default'...

Unit tests have much more advantages than disadvantages:

Advantages
----------

* Output of the test execution is clear
* Each test can be called individually
* Clearly separated from the source code (can also be a disadvantage)
* Fewer dependencies on the environment
* Each method of a test class is automatically called within a transaction
* No Unicode problems
* Individual tests can be subject to conditions

Disadvantages
-------------

* Creating the unit test requires more effort than creating doctests
* Also, a documentation of the source code, but not as obvious as the doctest

Different ways of running the tests
===================================

To get a more detailed output use the ``-v2`` option:

::

    Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
    Operations to perform:
      Synchronize unmigrated apps: crispy_forms, debug_toolbar, messages, staticfiles
      Apply all migrations: admin, auth, contenttypes, recipes, sessions
    Synchronizing apps without migrations:
      Creating tables...
        Running deferred SQL...
    Running migrations:
      Applying contenttypes.0001_initial... OK
      Applying auth.0001_initial... OK
      Applying admin.0001_initial... OK
      Applying admin.0002_logentry_remove_auto_add... OK
      Applying admin.0003_logentry_add_action_flag_choices... OK
      Applying contenttypes.0002_remove_content_type_name... OK
      Applying auth.0002_alter_permission_name_max_length... OK
      Applying auth.0003_alter_user_email_max_length... OK
      Applying auth.0004_alter_user_username_opts... OK
      Applying auth.0005_alter_user_last_login_null... OK
      Applying auth.0006_require_contenttypes_0002... OK
      Applying auth.0007_alter_validators_add_error_messages... OK
      Applying auth.0008_alter_user_username_max_length... OK
      Applying auth.0009_alter_user_last_name_max_length... OK
      Applying auth.0010_alter_group_name_max_length... OK
      Applying auth.0011_update_proxy_permissions... OK
      Applying recipes.0001_initial... OK
      Applying sessions.0001_initial... OK
    System check identified no issues (0 silenced).
    test_date_created_autoset (recipes.tests.RecipeSaveTests)
    Verifies date_created is autoset correctly. ... ok
    test_no_transaction (recipes.tests.RecipeSaveTests)
    Demonstrates skipIfDBFeature decorator. ... skipped 'Database has feature(s) supports_transactions'
    test_python_25 (recipes.tests.RecipeSaveTests)
    Demonstrates skipIf decorator. ... skipped 'Test runs only with Python 2.5 and lower'
    test_slug_is_unique (recipes.tests.RecipeSaveTests)
    Verifies if a slug is unique. ... ok

    ----------------------------------------------------------------------
    Ran 4 tests in 0.572s

    OK (skipped=2)
    Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...

Use the ``-v0`` option to hide most of the output, passing no arguments
to the ``test`` command executes all tests:

::

    $ python manage.py test -v0
    System check identified no issues (0 silenced).
    ----------------------------------------------------------------------
    Ran 4 tests in 0.567s

    OK (skipped=2)

You can also run the tests just for a single test case:

::

    $ python manage.py test recipes.tests.RecipeSaveTests
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    .ss.
    ----------------------------------------------------------------------
    Ran 4 tests in 0.621s

    OK (skipped=2)
    Destroying test database for alias 'default'...

And even for a single test method:

::

    $ python manage.py test recipes.tests.RecipeSaveTests.test_slug_is_unique
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.189s

    OK
    Destroying test database for alias 'default'...

You can also provide a path to a directory to discover tests below that directory:

::

    $ python manage.py test recipes/
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    .ss.
    ----------------------------------------------------------------------
    Ran 4 tests in 0.560s

    OK (skipped=2)
    Destroying test database for alias 'default'...

You can specify a custom filename pattern match using the ``-p`` (or ``--pattern``)
option, if your test files are named differently from the :file:`test*.py` pattern:

::

    $ ./manage.py test --pattern="tests_*.py"

Determining test coverage
=========================

Of course it is also important to know for which parts of the
application tests were already written. Here the Python package
`coverage <http://nedbatchelder.com/code/coverage/>`_ can help to
retrieve this information. It is not integrated in Django and
therefore must be manually installed::

    $ pip install coverage

Thus :program:`coverage` only examines our applications and not the
Framework you create the file :file:`.coveragerc` with the following
contents:

.. literalinclude:: ../src/cookbook_tests/.coveragerc
    :language: ini

Now you can create the data for the coverage report of the application
``recipes`` with the following command:

::

    $ coverage run manage.py test recipes
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    .ss.
    ----------------------------------------------------------------------
    Ran 4 tests in 0.625s

    OK (skipped=2)
    Destroying test database for alias 'default'...

Display the coverage data with this command in the shell:

::

    $ coverage report
    Name                               Stmts   Miss Branch BrPart  Cover   Missing
    ------------------------------------------------------------------------------
    cookbook/__init__.py                   0      0      0      0   100%
    cookbook/middleware.py                13      7      4      0    35%   13, 16-22
    recipes/__init__.py                    0      0      0      0   100%
    recipes/admin.py                       8      0      0      0   100%
    recipes/apps.py                        3      3      0      0     0%   1-5
    recipes/forms.py                       6      0      0      0   100%
    recipes/models.py                     43      3      2      1    91%   19, 54, 63, 57->59
    recipes/templatetags/__init__.py       0      0      0      0   100%
    recipes/templatetags/recipes.py       44     32      6      0    24%   19-31, 36-39, 42-50, 59-62, 67-72
    recipes/views.py                      72     30      2      0    57%   25-27, 39-52, 82-87, 90-92, 122-124, 127-129, 132-133
    userauth/__init__.py                   0      0      0      0   100%
    userauth/admin.py                      1      0      0      0   100%
    userauth/apps.py                       3      3      0      0     0%   1-5
    userauth/models.py                     1      0      0      0   100%
    userauth/views.py                     12      7      4      0    31%   9-16
    ------------------------------------------------------------------------------
    TOTAL                                206     85     18      1    54%

You can create a HTML coverage report with this command::

    $ coverage html

The HTML files are located in the directory :file:`htmlcov`.

Organizing tests as a package
=============================

Since the amount of tests is usually so large that a single file for all
test will quickly become confusing, it makes sense to organize the tests
as a Python package.

Create a new directory :file:`tests` inside the :file:`recipes`
directory and inside the new directory a file called :file:`__init__.py`::

    $ cd recipes
    $ mkdir tests
    $ touch tests/__init__.py

Now you move the file :file:`tests.py` in the new directory and
rename it to :file:`test_models.py`::

    $ mv tests.py tests/test_models.py

If you're still working on Python 2,  delete also the bytecode file
:file:`tests.py` so this does not prevent the execution of the code in the
:file:`tests` package::

    $ rm tests.pyc

Finally run the tests:

.. command-output:: python manage.py test recipes.tests.test_models
    :cwd: ../src/cookbook_tests_pkg

Functional tests (testing views)
================================

With the built-in Django test client an easy test browser is at your
disposal.

First we need some fixtures so that data in the front end is available
for testing.

Create a directory :file:`fixtures` in the directory :file:`recipes`:

::

    $ mkdir recipes/fixtures

Then you create a JSON file with the models of the recipes application::

    $ python manage.py dumpdata recipes --indent 4 --natural-foreign > recipes/fixtures/test_views_data.json

Now you create the file :file:`recipes/tests/test_views.py` with the
following content:

.. literalinclude:: ../src/cookbook_tests_pkg/recipes/tests/test_views.py
    :lines: 1-37

To extend the test suite for the front-end you can add the following
code to the ``RecipeViewsTests`` class. The
``RecipeViewsTests.test_add`` test needs an image. Add a random image to
the :file:`recipes/fixtures` directory and change the filename in the
code to match your file name.

.. literalinclude:: ../src/cookbook_tests_pkg/recipes/tests/test_views.py
    :lines: 39-

The front-end tests can be called explicitly with this command:

::

    $ python manage.py test recipes.tests.test_views
    Creating test database for alias 'default'...
    .....
    ----------------------------------------------------------------------
    Ran 5 tests in 0.620s

    OK
    Destroying test database for alias 'default'...
    System check identified no issues (0 silenced).

If you create now another coverage report you can see that the coverage for the views has increased:

::

    $ coverage run manage.py test recipes
    Creating test database for alias 'default'...
    .s.s.....
    ----------------------------------------------------------------------
    Ran 9 tests in 1.136s

    OK (skipped=2)
    Destroying test database for alias 'default'...
    System check identified no issues (0 silenced).

Display the coverage data with this command in the shell:

::

    $ coverage report
    Name                               Stmts   Miss Branch BrPart  Cover   Missing
    ------------------------------------------------------------------------------
    cookbook/__init__.py                   0      0      0      0   100%
    cookbook/middleware.py                13      4      4      1    59%   17-20, 16->17
    recipes/__init__.py                    0      0      0      0   100%
    recipes/admin.py                       8      0      0      0   100%
    recipes/apps.py                        3      3      0      0     0%   1-5
    recipes/forms.py                       6      0      0      0   100%
    recipes/models.py                     43      1      2      0    98%   54
    recipes/templatetags/__init__.py       0      0      0      0   100%
    recipes/templatetags/recipes.py       44      6      6      2    84%   21-22, 30, 45-46, 68, 26->30, 67->68
    recipes/views.py                      72     13      2      1    81%   25-27, 48-50, 122-124, 127-129, 132-133, 45->48
    userauth/__init__.py                   0      0      0      0   100%
    userauth/admin.py                      1      0      0      0   100%
    userauth/apps.py                       3      3      0      0     0%   1-5
    userauth/models.py                     1      0      0      0   100%
    userauth/views.py                     12      7      4      0    31%   9-16
    ------------------------------------------------------------------------------
    TOTAL                                206     37     18      4    79%

Further links to the Django documentation
=========================================

* :djangodocs:`Testing in Django <topics/testing/>`
