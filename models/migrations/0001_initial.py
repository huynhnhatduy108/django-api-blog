# Generated by Django 4.0.5 on 2022-07-13 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, db_column='title', max_length=75, null=True)),
                ('slug', models.CharField(blank=True, db_column='slug', max_length=100, null=True)),
                ('meta_title', models.CharField(blank=True, db_column='meta_title', max_length=100, null=True)),
                ('thumbnail', models.CharField(blank=True, db_column='thumbnail', max_length=500, null=True)),
                ('description', models.TextField(blank=True, db_column='description', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='updated_at', null=True)),
                ('hide_flag', models.IntegerField(blank=True, db_column='hide_flag', default=0, null=True)),
                ('deleted_flag', models.IntegerField(blank=True, db_column='deleted_flag', default=0, null=True)),
                ('parent', models.ForeignKey(blank=True, db_column='parent_id', null=True, on_delete=django.db.models.deletion.PROTECT, to='models.category')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('slug', models.CharField(blank=True, db_column='slug', max_length=50, null=True)),
                ('title', models.CharField(blank=True, db_column='title', max_length=100, null=True)),
                ('meta_title', models.CharField(blank=True, db_column='meta_title', max_length=100, null=True)),
                ('content', models.TextField(blank=True, db_column='content', null=True)),
                ('summary', models.TextField(blank=True, db_column='summary', null=True)),
                ('published_at', models.DateTimeField(blank=True, db_column='published_at', null=True)),
                ('thumbnail', models.CharField(blank=True, db_column='thumbnail', max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='updated_at', null=True)),
                ('hide_flag', models.IntegerField(blank=True, db_column='hide_flag', default=0, null=True)),
                ('deleted_flag', models.IntegerField(blank=True, db_column='deleted_flag', default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, db_column='title', max_length=75, null=True)),
                ('slug', models.CharField(blank=True, db_column='slug', max_length=100, null=True)),
                ('meta_title', models.CharField(blank=True, db_column='meta_title', max_length=100, null=True)),
                ('description', models.TextField(blank=True, db_column='description', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='updated_at', null=True)),
                ('hide_flag', models.IntegerField(blank=True, db_column='hide_flag', default=0, null=True)),
                ('deleted_flag', models.IntegerField(blank=True, db_column='deleted_flag', default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, db_column='username', max_length=50, null=True)),
                ('full_name', models.CharField(blank=True, db_column='full_name', max_length=50, null=True)),
                ('email', models.CharField(blank=True, db_column='email', max_length=200, null=True)),
                ('address', models.CharField(blank=True, db_column='address', max_length=200, null=True)),
                ('phone', models.CharField(blank=True, db_column='phone', max_length=50, null=True)),
                ('intro', models.TextField(blank=True, db_column='intro', null=True)),
                ('profile', models.TextField(blank=True, db_column='profile', null=True)),
                ('password', models.CharField(blank=True, db_column='password', max_length=50, null=True)),
                ('role', models.IntegerField(blank=True, db_column='role', default=0, null=True)),
                ('avatar_url', models.CharField(blank=True, db_column='avatar_url', max_length=500, null=True)),
                ('avatar_provider', models.CharField(blank=True, db_column='avatar_provider', max_length=500, null=True)),
                ('c_provider', models.CharField(blank=True, db_column='c_provider', max_length=50, null=True)),
                ('refresh_token', models.CharField(blank=True, db_column='refresh_token', max_length=500, null=True)),
                ('access_token', models.CharField(blank=True, db_column='access_token', max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='updated_at', null=True)),
                ('hide_flag', models.IntegerField(blank=True, db_column='hide_flag', default=0, null=True)),
                ('deleted_flag', models.IntegerField(blank=True, db_column='deleted_flag', default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='updated_at', null=True)),
                ('hide_flag', models.IntegerField(blank=True, db_column='hide_flag', default=0, null=True)),
                ('deleted_flag', models.IntegerField(blank=True, db_column='deleted_flag', default=0, null=True)),
                ('post', models.ForeignKey(blank=True, db_column='post_id', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='post_tag', to='models.post')),
                ('tag', models.ForeignKey(blank=True, db_column='tag_id', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tag_post', to='models.tag')),
            ],
        ),
        migrations.CreateModel(
            name='PostMeta',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('content', models.TextField(blank=True, db_column='content', null=True)),
                ('key', models.CharField(blank=True, db_column='meta_title', max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='updated_at', null=True)),
                ('hide_flag', models.IntegerField(blank=True, db_column='hide_flag', default=0, null=True)),
                ('deleted_flag', models.IntegerField(blank=True, db_column='deleted_flag', default=0, null=True)),
                ('post', models.ForeignKey(blank=True, db_column='post_id', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='post_meta', to='models.post')),
            ],
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, db_column='title', max_length=75, null=True)),
                ('content', models.TextField(blank=True, db_column='content', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='updated_at', null=True)),
                ('hide_flag', models.IntegerField(blank=True, db_column='hide_flag', default=0, null=True)),
                ('deleted_flag', models.IntegerField(blank=True, db_column='deleted_flag', default=0, null=True)),
                ('author', models.ForeignKey(blank=True, db_column='user_id', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='author_coment', to='models.user')),
                ('parent', models.ForeignKey(blank=True, db_column='parent_id', null=True, on_delete=django.db.models.deletion.PROTECT, to='models.postcomment')),
                ('post', models.ForeignKey(blank=True, db_column='post_id', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='post_coment', to='models.post')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='updated_at', null=True)),
                ('hide_flag', models.IntegerField(blank=True, db_column='hide_flag', default=0, null=True)),
                ('deleted_flag', models.IntegerField(blank=True, db_column='deleted_flag', default=0, null=True)),
                ('category', models.ForeignKey(blank=True, db_column='category_id', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='post_category', to='models.category')),
                ('post', models.ForeignKey(blank=True, db_column='post_id', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='post_category', to='models.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(blank=True, db_column='user_id', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='author_post', to='models.user'),
        ),
        migrations.AddField(
            model_name='post',
            name='parent',
            field=models.ForeignKey(blank=True, db_column='parent_id', null=True, on_delete=django.db.models.deletion.PROTECT, to='models.post'),
        ),
    ]
