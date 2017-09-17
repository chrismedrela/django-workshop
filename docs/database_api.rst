..  _database-api:

****************
The Database API
****************

Django brings a database API, which can create, read, write and delete
objects.

Backup your data and import the fixtures
========================================

So that you can perform all the operations you need exactly the same
data as used in the example. So you first have to make a backup of your
data, delete your existing data and then import the fixtures. At the end
you will restore your original data from the backup again.

..  note::

    You need the program `sqlite3 <http://www.sqlite.org/>`_ to use the
    :program:`dbshell` command. On Ubuntu, you can install it in terminal:

    ::

        $ sudo apt install sqlite3

This is how you create the backup:

::

    $ python manage.py dumpdata > backup.json

Now you can flush all tables in the database:

::

    $ python manage.py sqlflush | python manage.py dbshell

Make sure that we reset autoincrement counters, so that the user that we'll
create in a moment will have ID equals 1.

::

    $ echo "delete from sqlite_sequence" | python manage.py dbshell

Before you can import the data must create a superuser again:

::

    $ python manage.py createsuperuser

Now you have to import the data you're going to use in this exercise. You can
`find it in the Git repository of this project
<https://raw.githubusercontent.com/keimlink/django-workshop/4842c8c8a829472d9bdaaae0db2417ac1231ce9c/src/cookbook_tests/recipes/fixtures/recipes.json>`_
. If you have :command:`wget` installed you can download it from the command
line:

::

    $ wget -O import.json https://raw.githubusercontent.com/keimlink/django-workshop/4842c8c8a829472d9bdaaae0db2417ac1231ce9c/src/cookbook_tests/recipes/fixtures/recipes.json

If you can't click the URL or can't use :command:`wget` open
https://github.com/keimlink/django-workshop in your browser and navigate to
``src/cookbook_tests/recipes/fixtures/recipes.json``. If you are not at
revision ``4842c8c`` click on the "History" button and select ``4842c8c``. Now right-click on the
"Raw" button and click "Save Link As…".

Now you can import the data using the `loaddata` command:

::

    $ python manage.py loaddata import.json
    Installed 11 object(s) from 1 fixture(s)

Working with the Database API
=============================

A way to work with the database API is the Python interpreter. With the
following command you can start it:

::

    $ python manage.py shell

.. doctest::

    >>> from recipes.models import Category, Recipe  # import the models

    >>> # create a QuerySet with all recipes
    >>> all_recipes = Recipe.objects.all()
    >>> all_recipes
    <QuerySet [<Recipe: Aprikosenknödel>, <Recipe: Salat>, 
    <Recipe: Omas beste Frikadellen>, <Recipe: Aglio e Olio>, 
    <Recipe: Bratnudeln auf deutsche Art>]
    >>> # all_recipes is a QuerySet
    >>> type(all_recipes)
    <class 'django.db.models.query.QuerySet'>
    >>> all_recipes.count()
    5

    >>> # a list of all fields names of the Recipe model
    >>> [f.name for f in Recipe._meta.get_fields()]
    [u'id', 'title', 'slug', 'ingredients', 'preparation', 'time_for_preparation',
        'number_of_portions', 'difficulty', 'author', 'photo', 'date_created',
        'date_updated', 'category']

    >>> # look at single recipe from the QuerySet
    >>> all_recipes[1]
    <Recipe: Salat>
    >>> all_recipes[1].title
    u'Salat'
    >>> all_recipes[1].number_of_portions
    6

    >>> # create a new Category
    >>> salate = Category(name='Schnell Salate')
    >>> salate.id
    >>> salate.save()
    >>> salate.id
    7
    >>> salate.name
    'Schnell Salate'
    >>> salate.slug
    ''

    >>> # update the slug
    >>> from django.template.defaultfilters import slugify
    >>> slugify(salate.name)
    u'schnell-salate'
    >>> salate.slug = slugify(salate.name)
    >>> salate.save()
    >>> salate.slug
    u'schnell-salate'

    >>> # if a record can not be found an DoesNotExist Exception is raised
    >>> Category.objects.get(pk=23)
    Traceback (most recent call last):
        ...
    DoesNotExist: Category matching query does not exist.

    >>> # fetch a single model
    >>> Category.objects.get(pk=7)
    <Category: Schnell Salate>

    >>> # use the filter method
    >>> Category.objects.filter(name__startswith='Salate')
    <QuerySet []>
    >>> # only one object matches the following filter
    >>> Category.objects.filter(name__startswith='Schnell')
    <QuerySet [<Category: Schnell Salate>]>
    >>> # you can access one object from the queryset
    >>> Category.objects.filter(name__startswith='Schnell')[0]
    <Category: Schnell Salate>
    >>> categories = Category.objects.all()
    >>> categories.filter(name__startswith='Schnell')
    [<Category: Schnell Salate>]

    >>> # access recipes using a Category
    >>> categories[1]
    <Category: Hauptspeise>
    >>> type(categories[1].recipe_set)
    <class 'django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager'>
    >>> categories[1].recipe_set.all()
    <QuerySet [<Recipe: Omas beste Frikadellen>, <Recipe: Aglio e Olio>, 
    <Recipe: Bratnudeln auf deutsche Art>]>

    >>> # use the relation between Recipe and Category to create a new Category
    >>> recipe = all_recipes[0]
    >>> # this Recipe has one Category
    >>> recipe.category.all()
    <QuerySet [<Category: Party>]>
    >>> recipe.category.create(name='Foo')
    <Category: Foo>
    >>> # Now there are two Categories
    >>> recipe.category.all()
    <QuerySet [<Category: Party>, <Category: Foo>]>
    >>> # delete the new Category
    >>> foo = Category.objects.filter(name='Foo')
    >>> foo
    <QuerySet [<Category: Foo>]>
    >>> foo.delete()
    (2, {'recipes.Category': 1, 'recipes.Recipe_category': 1})
    >>> recipe.category.all()
    <QuerySet [<Category: Party>]>

    >>> # create complex queries using the Q object
    >>> # start with a simple filter
    >>> Recipe.objects.filter(number_of_portions=4)
    <QuerySet [<Recipe: Aprikosenknödel>, <Recipe: Aglio e Olio>, <Recipe: Bratnudeln auf deutsche Art>]>

    >>> # all Recipes that do not match the criteria
    >>> Recipe.objects.exclude(number_of_portions=4)
    <QuerySet [<Recipe: Salat>, <Recipe: Omas beste Frikadellen>]>

    >>> # the following query connects both filters using "AND"
    >>> Recipe.objects.filter(number_of_portions=4, title__startswith='B')
    <QuerySet [<Recipe: Bratnudeln auf deutsche Art>]>

    >>> # a Q object can also be used to create an "OR" connection
    >>> from django.db.models import Q
    >>> Recipe.objects.filter(Q(number_of_portions=4) | Q(title__startswith='K'))
    <QuerySet [<Recipe: Aprikosenknödel>, <Recipe: Aglio e Olio>, 
    <Recipe: Bratnudeln auf deutsche Art>]>

    >>> exit()

Display SQL queries
-------------------

If you want to display SQL queries that are executed in the shell, use the
following snippet of code:

::

    import logging
    l = logging.getLogger('django.db.backends')
    l.setLevel(logging.DEBUG)
    l.addHandler(logging.StreamHandler())

Delete the test data and restore the backup
===========================================

Now you delete the test data:

::

    $ python manage.py sqlflush | python manage.py dbshell

And restore the data from your backup:

::

    $ python manage.py loaddata backup.json

Further links to the Django documentation
=========================================

- :djangodocs:`Query API <topics/db/queries/>`
- :djangodocs:`QuerySet API <ref/models/querysets/>`
- :djangodocs:`Model _meta API <ref/models/meta/>`
