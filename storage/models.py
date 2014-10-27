from django.db import models

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

    class Meta:
        db_table = 'asset'


class AssetContent(models.Model):
    version = models.IntegerField(db_column='assetversion')
    tag = models.TextField()
    stream = models.ForeignKey('Stream', db_column='stream')

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


class Stream(models.Model):
    lobj = models.TextField(primary_key=True)  # This field type is a guess.
    signature = models.BinaryField(blank=True, null=True)

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
