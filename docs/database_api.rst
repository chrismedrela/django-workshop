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
    :program:`dbshell` command.

This is how you create the backup:

::

    $ python manage.py dumpdata > backup.json

Now you can flush all tables in the database:

::

    $ python manage.py sqlflush | python manage.py dbshell

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

::

    # import the models
    >>> from recipes.models import Category, Recipe

    # create a QuerySet with all recipes
    >>> all_recipes = Recipe.objects.all()
    >>> all_recipes
    [<Recipe: Bärlauchstrudel>, <Recipe: Kohleintopf mit Tortellini>,
        <Recipe: Käsespiegelei auf Spinatnudeln>]
    # all_recipes ist ein QuerySet
    >>> type(all_recipes)
    <class 'django.db.models.query.QuerySet'>
    >>> all_recipes.count()
    3

    # a list of all fields names of the Recipe model
    >>> [f.name for f in Recipe._meta.get_fields()]
    [u'id', 'title', 'slug', 'ingredients', 'preparation', 'time_for_preparation',
        'number_of_portions', 'difficulty', 'author', 'photo', 'date_created',
        'date_updated', 'category']

    # look at single recipe from the QuerySet
    >>> all_recipes[1]
    <Recipe: Kohleintopf mit Tortellini>
    >>> all_recipes[1].title
    u'Kohleintopf mit Tortellini'
    >>> all_recipes[1].number_of_portions
    4

    # create a new Category
    >>> salate = Category(name='Leckere Salate')
    >>> salate.id
    >>> salate.save()
    >>> salate.id
    7
    >>> salate.name
    'Leckere Salate'
    >>> salate.slug
    ''

    # update the slug
    >>> from django.template.defaultfilters import slugify
    >>> slugify(salate.name)
    u'leckere-salate'
    >>> salate.slug = slugify(salate.name)
    >>> salate.save()
    >>> salate.slug
    u'leckere-salate'

    # if a record can not be found an DoesNotExist Exception is raised
    >>> Category.objects.get(pk=23)
    Traceback (most recent call last):
        ...
    DoesNotExist: Category matching query does not exist.

    # fetch a single model
    >>> Category.objects.get(pk=7)
    <Category: Leckere Salate>

    # use the filter method
    >>> Category.objects.filter(name__startswith='Salate')
    []
    # Es wird ein QuerySet zurückgegeben
    >>> Category.objects.filter(name__startswith='Lecker')
    [<Category: Leckere Salate>]
    # So kann man direkt das Objekt bekommen
    >>> Category.objects.filter(name__startswith='Lecker')[0]
    <Category: Leckere Salate>
    # Auch auf ein QuerySet kann ein Filter angewendet werden
    >>> categories = Category.objects.all()
    >>> categories.filter(name__startswith='Lecker')
    [<Category: Leckere Salate>]

    # access recipes using a Category
    >>> categories[1]
    <Category: Pasta>
    >>> type(categories[1].recipe_set)
    <class 'django.db.models.fields.related.ManyRelatedManager'>
    >>> categories[1].recipe_set.all()
    [<Recipe: Kohleintopf mit Tortellini>, <Recipe: Käsespiegelei auf Spinatnudeln>]

    # use the relation between Recipe and Category to create a new Category
    >>> recipe = all_recipes[0]
    # this Recipe has three Categories
    >>> recipe.category.all()
    [<Category: Fleisch>, <Category: Backen>, <Category: Frühling>]
    >>> recipe.category.create(name='Foo')
    <Category: Foo>
    # Now there are four Categories
    >>> recipe.category.all()
    [<Category: Fleisch>, <Category: Backen>, <Category: Frühling>, <Category: Foo>]
    # delete the new Category
    >>> foo = Category.objects.filter(name='Foo')
    >>> foo
    [<Category: Foo>]
    >>> foo.delete()
    >>> recipe.category.all()
    [<Category: Fleisch>, <Category: Backen>, <Category: Frühling>]

    # create complex queries using the Q object
    # start with a simple filter
    >>> Recipe.objects.filter(number_of_portions=4)
    [<Recipe: Bärlauchstrudel>, <Recipe: Kohleintopf mit Tortellini>]

    # all Recipes that do not match the criteria
    >>> Recipe.objects.exclude(number_of_portions=4)
    [<Recipe: Käsespiegelei auf Spinatnudeln>]

    # the following query connects both filters using "AND"
    >>> Recipe.objects.filter(number_of_portions=4, title__startswith='K')
    [<Recipe: Kohleintopf mit Tortellini>]

    # a Q object can also be used to create an "OR" connection
    >>> from django.db.models import Q
    >>> Recipe.objects.filter(Q(number_of_portions=4) | Q(title__startswith='K'))
    [<Recipe: Bärlauchstrudel>, <Recipe: Kohleintopf mit Tortellini>,
        <Recipe: Käsespiegelei auf Spinatnudeln>]

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
