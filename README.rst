===============================
Unity Assets Server http client
===============================
.. image:: https://badge.fury.io/py/django-unity-asset-server-http-client.svg
    :target: http://badge.fury.io/py/django-unity-asset-server-http-client

.. contents:: :local:
   :depth: 2


LICENSE
-------
MIT

Requirements
------------

- python 2.7
- django 1.6+
- djangorestframework 2.4.3+
- django-filter 0.8

Quick start
-----------

1. Add "duashttp" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'duashttp',
    )

2. Add unity asset server router in your INSTALLED_APPS settings and configure
access to unity asset server access.

.. code-block:: python

  DATABASE_ROUTERS = ['duashttp.router.UnityAssetServerRouter', ]

.. code-block:: python

   DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
      },
      'unity_asset_server': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'game_project_database_name',
         'USER': 'admin',
         'PASSWORD': 'admin_password',
         'HOST': '192.168.0.1',  # There UNITY asset server is placed on
         'PORT': '10733'  # standard unity asset server port number
       }
   }


3. Manage your ``settings.py`` with django restframe work settings to
get optimal config:

.. code-block:: python


   REST_FRAMEWORK = {
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'page_size',
    # Maximum limit allowed when using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
   }

4. Apply your custom view sets or use existent and include them in "urls.py":

.. code-block:: python

   # -*- views.py -*-
   from duashttp.views.api import AssetVersionViewSetBase

   from rest_framework.decorators import list_route
   from rest_framework.response import Response

   from django.db.models import Q


   class AssetVersionViewSet(AssetVersionViewSetBase):
       """ AssetVersion view set """
       @list_route()
       def configs(self, request):
           """get xml configs with their last revision"""
           qset = (
               Q(name__icontains='.xml') &
               ~Q(name__icontains='(DEL_') &
               ~Q(name__icontains='~$')
           )
           xml_docs = self.queryset.filter(qset).order_by(
               'name', '-revision').distinct('name')
           docs = self.filter_queryset(xml_docs)
           page = self.paginate_queryset(docs)
           serializer = self.get_pagination_serializer(page)
           return Response(serializer.data)

.. code-block:: python

   # -*- urls.py -*-
   from django.conf.urls import patterns, include, url
   from views import *
   from rest_framework import routers

   router = routers.DefaultRouter()
   router.register(r'asset_versions', AssetVersionViewSet)


   urlpatterns = patterns('',
       # Examples:
       url(r'^api/', include(router.urls)),
       url(r'^api/', include(router.urls, namespace='api')),
   )

5. Start the development server and visit http://127.0.0.1:8000/api/
   to see available api calls.

Models
------
You can fetch data from unity asset server (based on posgres 8.3) using this:

.. code-block:: python

   >>> from duashttp.models import AssetVersion
   >>> versions = AssetVersion.objects.filter(name__icontains='Actions.xml')
   >>> versions
   ... [<AssetVersion: Actions.xml [46]>, <AssetVersion: Actions.xml [45]>,
   ... <AssetVersion: Actions.xml [44]>, <AssetVersion: Actions.xml [43]>,
   ... <AssetVersion: Actions.xml [42]>, <AssetVersion: Actions.xml [41]>,
   ... <AssetVersion: Actions.xml [40]>, <AssetVersion: Actions.xml [39]>,
   ... <AssetVersion: Actions.xml [38]>, <AssetVersion: Actions.xml [37]>,
   ... <AssetVersion: Actions.xml [36]>, <AssetVersion: Actions.xml [35]>,
   ... <AssetVersion: Actions.xml [34]>, '...(remaining elements truncated)...']
   >>> version = versions.get(revision=45)
   >>> print(version.get_blob_data())
   ... <?xml version="1.0" encoding="utf-8"?>
   ... <DocumentElement>
   ...     <Data_Table>
   ...         <id>1</id>
   ...         <num>1</num>
   ...         <prefab_name />
   ...         <small_prefab_name>SmallAction_gems_3_dollar</small_prefab_name>
   ...         <icon_sprite>lucky_gem</icon_sprite>
   ...         <is_small_action>1</is_small_action>
   ...         <is_big_action />
   ...         <is_top_panel_action />
   ...         <move_to_window />
   ...         <affected_id />
   ...         <appear_date>27/10/2014 08:00</appear_date>
   ...         <start_date>27/10/2014 08:00</start_date>
   ...         <end_date>31/10/2014 08:00</end_date>
   ...         <expire_date>31/10/2014 08:00</expire_date>
   ...         <source />
   ...         <patch />
   ...         <bind_id />
   ...     </Data_Table>
   ... </DocumentElement>

