.. index:: Install Django

**************
Install Django
**************

Before we install Django to start our first project we create a new virtualenv::

    $ mkvirtualenv django-workshop

If :program:`virtualenvwrapper` is not installed on your system you have to run
:program:`virtualenv` instead::

    $ virtualenv .virtualenvs/django-workshop

.. note::

    The command :program:`mkvirtualenv` activates the virtualenv
    automatically after it's created. If you used :program:`virtualenv`
    to create the virtualenv you to activate it manually::

        $ cd .virtualenvs/django-workshop
        $ . bin/activate

Alright, let's install Django::

    $ pip install Django

.. note:: Under Linux and Mac OS X root privileges may be required.

After a successful installation, you can check the Django version number
with the following command:

.. command-output:: django-admin.py --version

.. note::

    It could be that the file :file:`django_admin.py` is actually called
    :file:`django-admin`. That's not a problem, just leave off the
    extension ``.py``.

.. note::

    On Windows you may get an ``ImportError`` when you try to run
    :file:`django-admin.py`. This is because Windows does not run the
    Python interpreter from your virtual environment unless you invoke
    it directly. Instead, prefix all commands that use ``.py`` files
    with :program:`python` and use the full path to the file, like so:

    ::

        > python %USERPROFILE%\Envs\django-workshop\Scripts\django-admin.py

.. index:: timezones

Support for timezones
=====================

Starting with version 1.4, Django supports :djangodocs:`Timezones
<topics/i18n/timezones/#time-zones>`. This requires `pytz
<http://pytz.sourceforge.net/>`_ which should be installed along with Django.
You don't need to do any further steps in order to install it.
