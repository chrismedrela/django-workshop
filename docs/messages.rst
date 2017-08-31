********
Messages
********

Quite commonly in web applications, you need to display a one-time notification
message (also known as "flash message") to the user after processing a form or
some other types of user input.

For this, Django provides full support for cookie- and session-based messaging,
for both anonymous and authenticated users. The messages framework allows you to
temporarily store messages in one request and retrieve them for display in a
subsequent request (usually the next one). Every message is tagged with a
specific level that determines its priority (e.g., info, warning, or error).

Message framework is enabled by default and should be already configured
properly.

Creating new messages
=====================

When a user modifies a recipe, we'll display a message if it was successfully
updated. All we need to do is to call ``django.contrib.messages.success``
function.

::

    from django.contrib import messages 

    @login_required
    def edit(request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if recipe.author != request.user and not request.user.is_staff:
            raise PermissionDenied
        if request.method == 'POST':
            form = RecipeForm(instance=recipe, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'The recipe was updated.')
                return redirect(recipe)
        else:
            form = RecipeForm(instance=recipe)
        context = {'form': form, 'create': False, 'object': recipe}
        return render(request, 'recipes/form.html', context)

Modifying base template
=======================

We want to display on every page, therefore, we'll edit
``cookbook/templates/base.html`` template. Add the following code just after the
navigation bar:

..  code-block:: html+django

    <div>
      {% if messages %}
        {% for message in messages %}
          <div class="alert alert-{{message.tags}}">
            {{ message }}
          </div>
        {% endfor %}
      {% endif %}
    </div>

Further links to the Django documentation
=========================================

* :djangodocs:`The messages framework <ref/contrib/messages/>`

