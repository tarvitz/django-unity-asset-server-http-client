from django.db import models
import struct

# Create your models here.


class Databases(models.Model):
    database = models.TextField(blank=True, db_column='databasename')  # This field type is a guess.
    project = models.TextField(blank=True, db_column='projectname')
    description = models.TextField(blank=True)
    version = models.TextField(blank=True)

    class Meta:
        db_table = 'all_databases__view'


class ActiveUsers(models.Model):
    enabled = models.NullBooleanField()
    username = models.TextField(blank=True)  # This field type is a guess.
    realname = models.TextField(blank=True)
    email = models.TextField(blank=True)

    class Meta:
        db_table = 'all_users__view'


class Asset(models.Model):
    serial = models.IntegerField(primary_key=True)
    guid = models.BinaryField(max_length=128)

    def get_guid(self):
        """ gives int guid number instead of 01010.. sequence

        :rtype: int
        :return: guid
        """
        return int('0b%s' % self.guid, 2)

    class Meta:
        db_table = 'asset'


class AssetContent(models.Model):
    version = models.PositiveIntegerField(primary_key=True,
                                          db_column='assetversion')
    tag = models.TextField()
    stream = models.ForeignKey('storage.Stream', db_column='stream')

    versions = models.ForeignKey(
        'storage.AssetVersion', related_name='asset_content_version_set',
        db_column='assetversion'
    )

    class Meta:
        db_table = 'assetcontents'


class AssetType(models.Model):
    serial = models.IntegerField(primary_key=True)
    description = models.TextField(unique=True)

    class Meta:
        db_table = 'assettype'


class AssetVersion(models.Model):
    serial = models.IntegerField(primary_key=True)
    asset = models.ForeignKey(Asset, db_column='asset')
    parent = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True)
    variant = models.ForeignKey('storage.Variant', db_column='variant')
    revision = models.IntegerField()
    created_in = models.IntegerField()
    type = models.ForeignKey('storage.AssetType', db_column='assettype')
    digest = models.BinaryField(blank=True, null=True)

    def __unicode__(self):
        return '%s [%s]' % (self.name, self.revision)

    @property
    def contents(self):
        return self.asset_content_version_set

    def get_digest(self):
        """ return int uuid number for digest

        :rtype: int
        :return: digest
        """
        a, b = struct.unpack('>QQ', str(self.digest))
        return (a << 64) | b

    def get_blob_data(self, tag_target='asset', force=False):
        """
        get asset version content using pg large object streams

        :param bool force: False by default, forces get content from database
            instead of using cached value
        :rtype: str
        :return: content in raw format
        """
        if hasattr(self, '_blob_data') and not force:
            return self._blob_data

        self._blob_data = ''
        asset_contents = self.contents.filter(tag=tag_target)
        for asset_content in asset_contents:
            blobs = asset_content.stream.get_blobs()
            for blob in blobs:
                self._blob_data += str(blob.data)
        return self._blob_data

    class Meta:
        db_table = 'assetversion'
        ordering = ['-revision', ]


class ChangeSet(models.Model):
    serial = models.IntegerField(primary_key=True)
    description = models.TextField(blank=True)
    commit_time = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey('Person', db_column='creator')
    frozen = models.NullBooleanField()
    client_version = models.TextField(blank=True)

    class Meta:
        db_table = 'changeset'


class ChangeSetContent(models.Model):
    changeset = models.ForeignKey('storage.ChangeSet', db_column='changeset')
    asset_version = models.ForeignKey('storage.AssetVersion',
                                      db_column='assetversion', unique=True)

    class Meta:
        db_table = 'changesetcontents'


class ConfigurationMatview(models.Model):
    for_variant = models.IntegerField(blank=True, null=True)
    serial = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'configuration__matview'


class Person(models.Model):
    serial = models.IntegerField(primary_key=True)
    username = models.TextField(unique=True)
    active = models.BooleanField()

    class Meta:
        db_table = 'person'


class PersonRole(models.Model):
    person = models.IntegerField()
    role = models.IntegerField()

    class Meta:
        db_table = 'personroles'


class Reinheritance(models.Model):
    changeset = models.IntegerField()
    asset = models.IntegerField()

    class Meta:
        db_table = 'reinheritance'


class Role(models.Model):
    serial = models.IntegerField(primary_key=True)
    name = models.TextField(unique=True, blank=True)
    description = models.TextField(blank=True)
    automatic = models.NullBooleanField()

    class Meta:
        db_table = 'role'


class PGLargeObject(models.Model):
    loid = models.PositiveIntegerField(primary_key=True, db_column='loid')
    pageno = models.PositiveIntegerField()
    data = models.BinaryField(null=True, blank=True)
    stream = models.ForeignKey('storage.Stream', db_column='loid',
                               related_name='lo_stream_set')

    class Meta:
        db_table = 'pg_largeobject'


class Stream(models.Model):
    lobj = models.TextField(primary_key=True)
    signature = models.BinaryField(blank=True, null=True)


    @property
    def blobs(self):
        return self.lo_stream_set

    def get_blobs(self):
        return self.blobs.all()

    class Meta:
        db_table = 'stream'


class Variant(models.Model):
    serial = models.IntegerField(primary_key=True)
    name = models.TextField(unique=True)
    description = models.TextField(blank=True)
    base_variant = models.ForeignKey('self', db_column='base_variant',
                                     blank=True, null=True)
    basetime = models.DateTimeField(blank=True, null=True)
    dynamic = models.BooleanField()
    frozen = models.BooleanField()
    role = models.ForeignKey(Role, db_column='role', blank=True, null=True)

    class Meta:
        db_table = 'variant'


class VariantContent(models.Model):
    variant = models.ForeignKey('storage.Variant', db_column='variant')
    changeset = models.ForeignKey('storage.ChangeSet', db_column='changeset')

    class Meta:
        db_table = 'variantcontents'


class VariantInheritance(models.Model):
    child = models.ForeignKey('storage.Variant', db_column='child')
    parent = models.ForeignKey('storage.Variant', db_column='parent')
    depth = models.IntegerField()

    class Meta:
        db_table = 'variantinheritance'
