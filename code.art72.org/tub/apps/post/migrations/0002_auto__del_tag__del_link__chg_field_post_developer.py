# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Tag'
        db.delete_table('post_tag')

        # Removing M2M table for field post on 'Tag'
        db.delete_table('post_tag_post')

        # Deleting model 'Link'
        db.delete_table('post_link')

        # Adding M2M table for field links on 'Post'
        db.create_table('post_post_links', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm['post.post'], null=False)),
            ('link', models.ForeignKey(orm['utility.link'], null=False))
        ))
        db.create_unique('post_post_links', ['post_id', 'link_id'])

        # Adding M2M table for field tags on 'Post'
        db.create_table('post_post_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm['post.post'], null=False)),
            ('tag', models.ForeignKey(orm['utility.tag'], null=False))
        ))
        db.create_unique('post_post_tags', ['post_id', 'tag_id'])

        # Changing field 'Post.developer'
        db.alter_column('post_post', 'developer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['developer.Developer'], null=True))


    def backwards(self, orm):
        
        # Adding model 'Tag'
        db.create_table('post_tag', (
            ('text', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('post', ['Tag'])

        # Adding M2M table for field post on 'Tag'
        db.create_table('post_tag_post', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tag', models.ForeignKey(orm['post.tag'], null=False)),
            ('post', models.ForeignKey(orm['post.post'], null=False))
        ))
        db.create_unique('post_tag_post', ['tag_id', 'post_id'])

        # Adding model 'Link'
        db.create_table('post_link', (
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['post.Post'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('post', ['Link'])

        # Removing M2M table for field links on 'Post'
        db.delete_table('post_post_links')

        # Removing M2M table for field tags on 'Post'
        db.delete_table('post_post_tags')

        # Changing field 'Post.developer'
        db.alter_column('post_post', 'developer_id', self.gf('django.db.models.fields.related.ForeignKey')(default='Mr. Bar', to=orm['developer.Developer']))


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
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.ExtendedImage']", 'null': 'True', 'blank': 'True'}),
            'lat': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'long': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'medias': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['project.Media']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'process': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['project.Project']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'providers': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'repos': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['project.Repo']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'statement': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'post.post': {
            'Meta': {'object_name': 'Post'},
            'blurb': ('django.db.models.fields.TextField', [], {}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Mr. Bar'", 'to': "orm['developer.Developer']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'links': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['utility.Link']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['utility.Tag']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '144'})
        },
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

    complete_apps = ['post']
