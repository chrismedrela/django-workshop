.. _send_email:

**************
Sending Emails
**************

Django has built-in support for sending emails. We'll send an email to us when a
new user registers. We'll use ``django.core.mail.send_email`` function. We need
only to alter ``register`` view:

::

    from django.core.mail import send_mail

    def register(request, template_name='userauth/register.html', next_page_name='/'):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                send_mail(
                    'A new user has registered',
                    'Here is the message',
                    'from@email.com',
                    ['your@email.com'],
                    fail_silently=False,
                )
                return HttpResponseRedirect(reverse(next_page_name))
        else:
            form = UserCreationForm()
        return render(request, template_name, {'form': form})

Mail is sent using the SMTP host and port specified in the ``EMAIL_HOST`` and
``EMAIL_PORT`` settings. The ``EMAIL_HOST_USER`` and ``EMAIL_HOST_PASSWORD``
settings, if set, are used to authenticate to the SMTP server, and the
``EMAIL_USE_TLS`` and ``EMAIL_USE_SSL`` settings control whether a secure
connection is used.

Let's add the following line to ``cookbook/local_settings.py``, so that Django
don't send real emails. Instead, they'll be printed on the console, which is
very convenient in development mode.

::

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

Further links to the Django documentation
=========================================

- :djangodocs:`Sending email <topics/email>`
