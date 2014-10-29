===============================
Unity Assets Server http client
===============================

.. contents:: :local:
   :depth: 2


TODO
----

- make possible download searched asset with HTTP 1.1 request (REST-api)

LICENSE
-------
MIT

Requirements
------------

- python 2.7
- django 1.6+

see ``requirements/base.txt`` for virtualenv/pip installation

- ``requirements/all.txt`` - all requirements with dev deps
- ``requirements/base.txt`` - base requirements
- ``requirements/dev.txt`` - development related packages

Fast USE
--------
You can fetch data from unity asset server (based on posgres 8.3) using this:

.. code-block:: python

   >>> from storage.models import AssetVersion
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

