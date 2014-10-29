from django.conf.urls import patterns, include, url
from django.contrib import admin

from storage.views.api import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'asset_versions', AssetVersionViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'assettools.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(router.urls, namespace='api')),
)
