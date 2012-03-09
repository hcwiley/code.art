# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ExternalId'
        db.create_table('developer_externalid', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('handle', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('developer', ['ExternalId'])

        # Deleting field 'Developer.vimeo_id'
        db.delete_column('developer_developer', 'vimeo_id')

        # Deleting field 'Developer.github_id'
        db.delete_column('developer_developer', 'github_id')

        # Deleting field 'Developer.source_forge_id'
        db.delete_column('developer_developer', 'source_forge_id')

        # Deleting field 'Developer.twitter_id'
        db.delete_column('developer_developer', 'twitter_id')

        # Deleting field 'Developer.bitbucket_id'
        db.delete_column('developer_developer', 'bitbucket_id')

        # Deleting field 'Developer.youtube_id'
        db.delete_column('developer_developer', 'youtube_id')

        # Deleting field 'Developer.stack_over_id'
        db.delete_column('developer_developer', 'stack_over_id')


    def backwards(self, orm):
        
        # Deleting model 'ExternalId'
        db.delete_table('developer_externalid')

        # Adding field 'Developer.vimeo_id'
        db.add_column('developer_developer', 'vimeo_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True), keep_default=False)

        # Adding field 'Developer.github_id'
        db.add_column('developer_developer', 'github_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True), keep_default=False)

        # Adding field 'Developer.source_forge_id'
        db.add_column('developer_developer', 'source_forge_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True), keep_default=False)

        # Adding field 'Developer.twitter_id'
        db.add_column('developer_developer', 'twitter_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True), keep_default=False)

        # Adding field 'Developer.bitbucket_id'
        db.add_column('developer_developer', 'bitbucket_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True), keep_default=False)

        # Adding field 'Developer.youtube_id'
        db.add_column('developer_developer', 'youtube_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True), keep_default=False)

        # Adding field 'Developer.stack_over_id'
        db.add_column('developer_developer', 'stack_over_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True), keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'developer.developer': {
            'Meta': {'object_name': 'Developer'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'lat': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'long': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'statement': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'developer.externalid': {
            'Meta': {'object_name': 'ExternalId'},
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['developer']
