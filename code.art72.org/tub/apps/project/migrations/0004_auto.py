# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding M2M table for field dependencies on 'Repo'
        db.create_table('project_repo_dependencies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('repo', models.ForeignKey(orm['project.repo'], null=False)),
            ('link', models.ForeignKey(orm['utility.link'], null=False))
        ))
        db.create_unique('project_repo_dependencies', ['repo_id', 'link_id'])

        # Adding M2M table for field tags on 'Repo'
        db.create_table('project_repo_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('repo', models.ForeignKey(orm['project.repo'], null=False)),
            ('tag', models.ForeignKey(orm['utility.tag'], null=False))
        ))
        db.create_unique('project_repo_tags', ['repo_id', 'tag_id'])


    def backwards(self, orm):
        
        # Removing M2M table for field dependencies on 'Repo'
        db.delete_table('project_repo_dependencies')

        # Removing M2M table for field tags on 'Repo'
        db.delete_table('project_repo_tags')


    models = {
        'project.extendedimage': {
            'Meta': {'object_name': 'ExtendedImage'},
            'external': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded': ('sorl.thumbnail.fields.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'project.media': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Media'},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['project.ExtendedImage']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '144'}),
            'video': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '400', 'null': 'True', 'blank': 'True'})
        },
        'project.project': {
            'Meta': {'object_name': 'Project'},
            'blurb': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
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
            'dependencies': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['utility.Link']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['utility.Tag']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '144'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'utility.link': {
            'Meta': {'object_name': 'Link'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'utility.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['project']
