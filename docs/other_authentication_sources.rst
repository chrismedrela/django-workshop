****************************
Other Authentication Sources
****************************

An alternative authentication can be implemented in the file
:file:`userauth/backends.py` as follows::

    from django.conf import settings
    from django.contrib.auth.models import User


    class SettingsBackend():
        """Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

        Use the login name, and password in plain text. This example uses "admin"
        as username and password:

        ADMIN_LOGIN = 'admin'
        ADMIN_PASSWORD = 'sha1$4e987$afec41beb01610c713124cac668d0becc75b4d4c'
        """
        def authenticate(self, username=None, password=None):
            login_valid = (settings.ADMIN_LOGIN == username)
            pwd_valid = (password == settings.ADMIN_PASSWORD)
            if login_valid and pwd_valid:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    # Create a new user.
                    user = User(username=username)
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                return user
            return None

        def get_user(self, user_id):
            try:
                return User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return None

To use the ``SettingsBackend`` the following setting has to be added to
:file:`cookbook/settings.py`::

    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'userauth.backends.SettingsBackend',
    ]

Further links to the Django documentation
=========================================

* :djangodocs:`Other authentication sources <topics/auth/customizing/#other-authentication-sources>`
