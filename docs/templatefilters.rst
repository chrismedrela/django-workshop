..  _templatefilters:

****************
Template Filters
****************

There are two basic concepts in Django templates: tags and filters. We have
already learned how we can write our own template tag. Now we will focus on
creating our own filter.

Filters let you alter a value before rendering it:

..  code-block:: html+django

    {{ some_html|safe }}

Filters can accept an additional argument:

..  code-block:: html+django

    {{ some_datetime_object|date:"D d M Y" }}

Listify ingredients
===================

We'll create a filter that takes ingredients list as a string and convert it
into an unordered list -- we assume that users put each ingredient in a new
line. Then, every line is converted into one list item. This filter doesn't take
any additional argument.

We'll put the filter implementation in ``recipes/templatetags/recipes.py`` file:

::

    from django.template import loader
    from django.template.defaultfilters import stringfilter

    @register.filter
    @stringfilter
    def listify(value):
        items = value.split('\n')
        template = loader.get_template('recipes/listify.html')
        rendered = template.render({'items': items})
        return rendered

We use ``@stringfilter`` to make sure that the value passed to the filter is a
string. If it's of a different type (i.e. an integer), it'll be converted into a
string before passing it to the filter.

What we do inside the filter is that we split the value which is ingredients
list as a one huge string, and then we split it by lines. Then, we pass this
list into ``recipes/listify.html`` template. We need to create this template:

..  code-block:: html+django

    <ul class="list-group">
      {% for item in items %}
        <li class="list-group-item">{{ item }}</li>
      {% endfor %}
    </ul>

At the end, we need to use this filter in
``recipes/templates/recipes/detail.html`` file:

..  code-block:: html+django

    <h3>Ingredients</h3>
    {{ object.ingredients|listify }}

Shorten page elements
=====================

The list of ingredients is widen to fit entire page. However, we may want to
shorten it, so that it uses only some part of the available width. We'll write a
filter that takes any HTML as a string and put it into a column. An additional
argument determines the width of the column.

We'll put the filter implementation in ``recipes/templatetags/recipes.py`` file:

::

    @register.filter(name='shorten')
    @stringfilter
    def shorten(value, width):
        if not 1 <= width <= 12:
            raise ValueError('Invalid width: {}'.format(width))

        template = loader.get_template('recipes/shorten.html')
        rendered = template.render({'content': value, 'width': width})
        return rendered

You can see that you can specify the filter name in ``@register.filter``
decorator. If you don't do this, the filter name is the same as the name of the
function.

We need to create ``recipes/templates/recipes/shorten.html`` template:

..  code-block:: html+django

    <div class="row">
      <div class="col-sm-{{ width }}">
        {{ content }}
      </div>
    </div>

At the end, we need to use this filter in
``recipes/templates/recipes/detail.html`` file:

..  code-block:: html+django

    <h3>Ingredients</h3>
    {{ object.ingredients|listify|shorten:4 }}

Further links to the Django documentation
=========================================

* :djangodocs:`Writing custom template filters <howto/custom-template-tags/#writing-custom-template-filters>`
