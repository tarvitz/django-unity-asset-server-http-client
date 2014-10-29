# coding: utf-8
from django_filters import FilterSet
from storage.models import AssetVersion


class AssetVersionFilter(FilterSet):
    class Meta:
        model = AssetVersion
        fields = {
            'name': ['icontains', 'iexact'],
            'revision': ['exact'],
        }
