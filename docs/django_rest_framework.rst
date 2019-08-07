*********************
Django Rest Framework
*********************

Django REST framework is a powerful and flexible toolkit for building Web APIs.

Some reasons you might want to use REST framework:

- The Web browsable API is a huge usability win for your developers.

- Authentication policies including packages for OAuth1a and OAuth2.

- Serialization that supports both ORM and non-ORM data sources.

- Customizable all the way down - just use regular function-based views if you
  don't need the more powerful features.

- Extensive documentation, and great community support.

- Used and trusted by internationally recognised companies including Mozilla,
  Red Hat, Heroku, and Eventbrite.

Installation
============

Install using ``pip``::

    pip install djangorestframework

Add ``rest_framework`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = [
        ...
        'rest_framework',
    ]

Basic Configuration
===================

Any global settings for a REST framework API are kept in a single configuration
dictionary named REST_FRAMEWORK. Start off by adding the following to your
settings.py module::

    REST_FRAMEWORK = {
        # Settings for pagination:
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 3,
    }

Add serializers to ``recipes/rest_serializers.py`` file::

    from rest_framework import serializers

    from recipes.models import Recipe, Category


    class CategorySerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Category
            fields = ['url', 'name', 'slug', 'description']


    class RecipeSerializer(serializers.HyperlinkedModelSerializer):
        author = serializers.SlugRelatedField(
            queryset=User.objects.all(), slug_field='username')

        class Meta:
            model = Recipe
            fields = [
                'url', 'title', 'slug', 'ingredients',
                'preparation', 'time_for_preparation', 'number_of_portions',
                'difficulty', 'category', 'author', 'photo', 
                'date_created', 'date_updated',
            ]

Add views to ``recipes/rest_views.py`` file::

    from rest_framework import viewsets

    from .rest_serializers import RecipeSerializer, CategorySerializer
    from .models import Recipe, Category


    class RecipeViewSet(viewsets.ModelViewSet):
        """
        API endpoint that allows recipes to be viewed or edited.
        """
        queryset = Recipe.objects.all().order_by('-date_created')
        serializer_class = RecipeSerializer


    class CategoryViewSet(viewsets.ModelViewSet):
        """
        API endpoint that allows categories to be viewed or edited.
        """
        queryset = Category.objects.all().order_by('-slug')
        serializer_class = CategorySerializer

Add urls to ``recipes/rest_urls.py`` file::

    from django.urls import include, path
    from rest_framework import routers

    from . import rest_views

    router = routers.DefaultRouter()
    router.register('recipes', rest_views.RecipeViewSet)
    router.register('categories', rest_views.CategoryViewSet)

    # Wire up our API using automatic URL routing.
    # Additionally, we include login URLs for the browsable API.
    urlpatterns = [
        path('api/', include(router.urls)),
        # REST framework's login and logout views:
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    ]

Include the above file in the global URL configuration in ``cookbook/urls.py``::

    import recipes.rest_urls

    urlpatterns = [
        ...
        path('', include(recipes.rest_urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

Let's add support for YAML, that is human readable JSON. Install it::

    $ pip install djangorestframework-yaml

And modify your REST framework settings::

    REST_FRAMEWORK = {
        ...
        'DEFAULT_PARSER_CLASSES': [
            'rest_framework.parsers.JSONParser',
            'rest_framework.parsers.FormParser',
            'rest_framework.parsers.MultiPartParser',
            'rest_framework_yaml.parsers.YAMLParser',
        ],
        'DEFAULT_RENDERER_CLASSES': [
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',        
            'rest_framework_yaml.renderers.YAMLRenderer',
        ],
    }

Serializers
===========

Serializers are very similar to Forms. There are Serializers and
ModelSerializers, the same way there are Forms and ModelForms. The former are
not tied to any Model and you need to define all fields and create() and
update() methods. The latter can reuse information from your model and save you
time.

So far, we used ModelSerializers. Let's see how we can do the same with pure
Serializers. Add to ``recipes/rest_serializers.py``::

    from rest_framework.validators import UniqueValidator
    
    from django.db import models
    
    class CategoryPureSerializer(serializers.Serializer):
        url = serializers.HyperlinkedIdentityField(view_name='category-detail')
        name = serializers.CharField(max_length=100)
        slug = serializers.SlugField(allow_unicode=False, max_length=50,
            validators=[UniqueValidator(queryset=Category.objects.all())])
        description = serializers.CharField(allow_blank=True, required=False, style={'base_template': 'textarea.html'})
        
        def create(self, validated_data):
            return Category.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.slug = validated_data.get('slug', instance.slug)
            instance.description = validated_data.get('description', instance.description)
            instance.save()
            return instance    

Modify ``rest_views.py`` to use ``CategoryPureSerializer`` instead of the
original ``CategorySerializer``::

    from .rest_serializers import RecipeSerializer, CategorySerializer, CategoryPureSerializer

    class CategoryViewSet(viewsets.ModelViewSet):
        ...
        serializer_class = CategoryPureSerializer

To avoid repetition, it's better to use model-based Serializers when it's
possible. ModelSerializers automatically determines set of fields and implement
create() and update() methods.

Serializers print programmer-friendly self-description::

    >>> CategorySerializer()
    CategorySerializer():
        url = HyperlinkedIdentityField(view_name='category-detail')
        name = CharField(max_length=100)
        slug = SlugField(allow_unicode=False, max_length=50, validators=[<UniqueValidator(queryset=Category.objects.all())>])
        description = CharField(allow_blank=True, required=False, style={'base_template': 'textarea.html'})

Go to ``http://127.0.0.1:8000/api``. Discover and test your API.

Requests and Responses
======================

REST framework introduces a ``Request`` object that extends the regular ``HttpRequest``,
and provides more flexible request parsing. The core functionality of the
``Request`` object is the ``request.data`` attribute, which is similar to ``request.POST``,
but more useful for working with Web APIs.

REST framework also introduces a ``Response`` object, which is a type of
``TemplateResponse`` that takes unrendered content and uses content negotiation to
determine the correct content type to return to the client.

So far we used automatic ViewSets that did most of work for us. Let's create
function-based views for Category model in ``recipes/rest_views.py``::

    from rest_framework import status
    from rest_framework.decorators import api_view
    from rest_framework.response import Response

    ...

    @api_view(['GET', 'POST'])
    def category_list(request):
        if request.method == 'GET':
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True, context={'request':request})
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = CategorySerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @api_view(['GET', 'PUT', 'DELETE'])
    def category_detail(request, pk):
        """
        Retrieve, update or delete a code snippet.
        """
        try:
            snippet = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = CategorySerializer(snippet, context={'request':request})
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = CategorySerializer(snippet, data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

We need to register these views in ``recipes/rest_urls.py``::

    urlpatterns = [
        path('api/manual-category/', rest_views.category_list),
        path('api/manual-category/<int:pk>/', rest_views.category_detail),
        ...
    ]

Test these views in your browser:
``http://127.0.0.1:8000/api/manual-category/``. You can see it's still
discoverable thanks to using ``@api_view``, ``Request`` and ``Response``
classes.

Class Based Views
=================

Let's rewrite our views using class-based views::

    from rest_framework.views import APIView

    ...

    class CategoryList(APIView):
        def get(self, request, format=None):
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True, context={'request': request})
            return Response(serializer.data)

        def post(self, request, format=None):
            serializer = CategorySerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    class CategoryDetail(APIView):
        def get_object(self, pk):
            try:
                return Category.objects.get(pk=pk)
            except Category.DoesNotExist:
                raise Http404

        def get(self, request, pk, format=None):
            category = self.get_object(pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)

        def put(self, request, pk, format=None):
            category = self.get_object(pk)
            serializer = CategorySerializer(category, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def delete(self, request, pk, format=None):
            category = self.get_object(pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

We need to register our views::

    urlpatterns = [ 
        path('api/class-based-category/', rest_views.CategoryList.as_view()),
        path('api/class-based-category/<int:pk>/', rest_views.CategoryDetail.as_view()),
        ...
    ]

One of the big wins of using class-based views is that it allows us to easily
compose reusable bits of behaviour.

The create/retrieve/update/delete operations that we've been using so far are
going to be pretty similar for any model-backed API views we create. Those bits
of common behaviour are implemented in REST framework's mixin classes.

Here are our new classes::

    from rest_framework import mixins
    from rest_framework import generics

    class CategoryList(
            mixins.ListModelMixin,
            mixins.CreateModelMixin,
            generics.GenericAPIView,
    ):
        queryset = Category.objects.all()
        serializer_class = CategorySerializer

        def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)

        def post(self, request, *args, **kwargs):
            return self.create(request, *args, **kwargs)

    class CategoryDetail(
            mixins.RetrieveModelMixin,
            mixins.UpdateModelMixin,
            mixins.DestroyModelMixin,
            generics.GenericAPIView,
    ):
        queryset = Category.objects.all()
        serializer_class = CategorySerializer

        def get(self, request, *args, **kwargs):
            return self.retrieve(request, *args, **kwargs)

        def put(self, request, *args, **kwargs):
            return self.update(request, *args, **kwargs)

        def delete(self, request, *args, **kwargs):
            return self.destroy(request, *args, **kwargs)

Or we can use builtin classes::

    class CategoryList(generics.ListCreateAPIView):
        queryset = Category.objects.all()
        serializer_class = CategorySerializer


    class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
        queryset = Category.objects.all()
        serializer_class = CategorySerializer

We'll move even more further by replacing these views with viewsets.

REST framework includes an abstraction for dealing with ``ViewSets``, that allows
the developer to concentrate on modeling the state and interactions of the API,
and leave the URL construction to be handled automatically, based on common
conventions.

``ViewSet`` classes are almost the same thing as ``View`` classes, except that they
provide operations such as ``read``, or ``update``, and not method handlers such as ``get``
or ``put``.

A ``ViewSet`` class is only bound to a set of method handlers at the last moment,
when it is instantiated into a set of views, typically by using a ``Router`` class
which handles the complexities of defining the URL conf for you.

::

    from rest_framework import permissions
    from rest_framework.decorators import action

    from .rest_permissions import IsOwnerOrReadOnly

    class RecipeViewSet(viewsets.ModelViewSet):
        """
        API endpoint that allows recipes to be viewed or edited.
        """
        queryset = Recipe.objects.all().order_by('-date_created')
        serializer_class = RecipeSerializer
        permission_classes = [
            permissions.IsAuthenticatedOrReadOnly,
            IsOwnerOrReadOnly,
        ]

        @action(detail=True)
        def tldr(self, request, *args, **kwargs):
            recipe = self.get_object()
            return Response({'slug': recipe.slug, 'title': recipe.title})

        def perform_create(self, serializer):
            serializer.save(author=self.request.user)

Authentication and Permission
=============================

Currently our API doesn't have any restrictions on who can edit or delete code
snippets. Let's secure our API::

    from rest_framework import permissions

    from .rest_permissions import IsOwnerOrReadOnly


    class RecipeSerializer(serializers.HyperlinkedModelSerializer):
        author = serializers.CharField(read_only=True, source='author.username')

        permission_classes = [
            permissions.IsAuthenticatedOrReadOnly, 
            IsOwnerOrReadOnly,
        ]

        class Meta:
            model = Recipe
            fields = [
                'url', 'title', 'slug', 'ingredients',
                'preparation', 'time_for_preparation', 'number_of_portions',
                'difficulty', 'category', 'author', 'photo', 
                'date_created', 'date_updated',
            ]

Create a new file ``recipes/rest_permissions.py``::

    from rest_framework import permissions


    class IsOwnerOrReadOnly(permissions.BasePermission):
        """
        Custom permission to only allow owners of an object to edit it.
        """

        def has_object_permission(self, request, view, obj):
            # Read permissions are allowed to any request,
            # so we'll always allow GET, HEAD or OPTIONS requests.
            if request.method in permissions.SAFE_METHODS:
                return True

            # Write permissions are only allowed to the author of the recipe.
            return obj.author == request.user

Modify ``recipes/rest_views.py``::

    class RecipeViewSet(viewsets.ModelViewSet):
        ...
        def perform_create(self, serializer):
            serializer.save(author=self.request.user)

Use http://www.cdrf.co for easier navigation of all class-based views.
