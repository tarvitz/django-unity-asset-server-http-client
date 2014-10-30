# coding: utf-8
from duashttp.models import AssetVersion

from rest_framework import serializers


class AssetVersionSerializer(serializers.HyperlinkedModelSerializer):
    hash = serializers.SerializerMethodField('get_digest')
    guid = serializers.SerializerMethodField('get_guid')

    def get_digest(self, obj):
        return str(hex(obj.get_digest())).replace('0x', '').replace('L', '')

    def get_guid(self, obj):
        guid = obj.asset.get_guid()
        return str(hex(guid)).replace('0x', '').replace('L', '')

    class Meta:
        model = AssetVersion
        fields = ('serial', 'name', 'revision', 'created_in', 'hash', 'guid')
