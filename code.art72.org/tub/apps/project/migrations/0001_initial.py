# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Repo'
        db.create_table('project_repo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=144)),
            ('blurb', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('project', ['Repo'])

        # Adding model 'ExtendedImage'
        db.create_table('project_extendedimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uploaded', self.gf('sorl.thumbnail.fields.ImageField')(default=None, max_length=100, null=True, blank=True)),
            ('external', self.gf('django.db.models.fields.URLField')(default='', max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('project', ['ExtendedImage'])

        # Adding model 'Media'
        db.create_table('project_media', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=144)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['project.ExtendedImage'], null=True, blank=True)),
            ('video', self.gf('django.db.models.fields.URLField')(default=None, max_length=200, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('project', ['Media'])

        # Adding model 'Project'
        db.create_table('project_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=144)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=50, db_index=True)),
            ('blurb', self.gf('django.db.models.fields.TextField')()),
            ('use_git_blurb', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.ExtendedImage'], null=True, blank=True)),
        ))
        db.send_create_signal('project', ['Project'])

        # Adding M2M table for field repos on 'Project'
        db.create_table('project_project_repos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['project.project'], null=False)),
            ('repo', models.ForeignKey(orm['project.repo'], null=False))
        ))
        db.create_unique('project_project_repos', ['project_id', 'repo_id'])

        # Adding M2M table for field media on 'Project'
        db.create_table('project_project_media', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['project.project'], null=False)),
            ('media', models.ForeignKey(orm['project.media'], null=False))
        ))
        db.create_unique('project_project_media', ['project_id', 'media_id'])


    def backwards(self, orm):
        
        # Deleting model 'Repo'
        db.delete_table('project_repo')

        # Deleting model 'ExtendedImage'
        db.delete_table('project_extendedimage')

        # Deleting model 'Media'
        db.delete_table('project_media')

        # Deleting model 'Project'
        db.delete_table('project_project')

        # Removing M2M table for field repos on 'Project'
        db.delete_table('project_project_repos')

        # Removing M2M table for field media on 'Project'
        db.delete_table('project_project_media')


    models = {
        'project.extendedimage': {
            'Meta': {'object_name': 'ExtendedImage'},
            'external': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded': ('sorl.thumbnail.fields.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'project.media': {
            'Meta': {'object_name': 'Media'},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['project.ExtendedImage']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '144'}),
            'video': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'project.project': {
            'Meta': {'object_name': 'Project'},
            'blurb': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.ExtendedImage']", 'null': 'True', 'blank': 'True'}),
            'media': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['project.Media']", 'null': 'True', 'blank': 'True'}),
            'repos': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['project.Repo']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '144'}),
            'use_git_blurb': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'project.repo': {
            'Meta': {'object_name': 'Repo'},
            'blurb': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '144'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['project']
