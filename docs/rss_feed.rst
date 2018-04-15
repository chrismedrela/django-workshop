********
RSS Feed
********

The app "news" we created in the chapter :ref:`multiple_databases` has
currently no front-end and will therefore get a
`RSS Feed <https://en.wikipedia.org/wiki/RSS>`_.

Create the Feed
===============

For this you create first :file:`news/feeds.py`:

.. literalinclude:: ../src/cookbook_multi_db/news/feeds.py
    :linenos:

Since we are reading the number of elements in the RSS feed from the
file :file:`settings.py` we must also define it there::

    NEWS_FEED_COUNT = 5

Define the URL for the feed
===========================

Then you create the ``URLconf`` in :file:`news/urls.py`:

.. literalinclude:: ../src/cookbook_multi_db/news/urls.py
    :linenos:

And add it afterwards to the ``URLConf`` in :file:`cookbook/urls.py`:

.. literalinclude:: ../src/cookbook_multi_db/cookbook/urls.py
    :lines: 10-15
    :emphasize-lines: 4

Make sure that ``News`` model in :file:`news/models.py`
has ``get_absolute_url`` method:

.. literalinclude:: ../src/cookbook_multi_db/news/models.py
    :lines: 20-21

Do not forget about this import:

.. literalinclude:: ../src/cookbook_multi_db/news/models.py
    :lines: 3

Write the Views
===============

Now you create the (very simple) views for the feed in :file:`news/views.py`:

.. literalinclude:: ../src/cookbook_multi_db/news/views.py
    :linenos:

Create Templates
================

And at the end you put on the new templates and will broaden the existing.

First, expand the template :file:`templates/base.html` to the entry for
the feed::

    <head>
        ...
        <link rel="alternate" type="application/rss+xml"
              title="News from the cookbook" href="{% url 'news_article_feed' %}" />
    </head>

Many browsers show the link to the RSS feed in the address bar only
after the installation of additional extensions. Therefore, it may be
useful to add the link to RSS feed also to the ``body`` of the page::

    <div id="navbar" class="navbar-collapse collapse">
        ...
        <ul class="nav navbar-nav">
            <li><a href="{% url 'news_article_feed' %}">RSS Feed</a></li>
        </ul>
    </div>

Then, create the template for the list elements of the feed in
:file:`news/templates/news/article_list.html`. The filter
``truncatewords`` only displays the first ten words of the message text:

.. literalinclude:: ../src/cookbook_multi_db/news/templates/news/article_list.html
    :linenos:
    :language: html+django

And finally you create the template for a feed element in
:file:`news/templates/news/article_detail.html`:

.. literalinclude:: ../src/cookbook_multi_db/news/templates/news/article_detail.html
    :linenos:
    :language: html+django

Customizing the Site
====================

Thus, the links in the RSS feed also work, yet the site must be adjusted
in the admin. Open the list of sites in the admin and select the site
with the domain name ``example.com`` for editing. Instead of
``example.com`` you must use ``127.0.0.1:8000`` as domain name. The
display name may not necessarily be changed - but it does not hurt.

Further links to the Django documentation
=========================================

* :djangodocs:`Syndication feeds (RSS/Atom) <ref/contrib/syndication/>`
