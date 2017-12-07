# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import django.core.validators
import tinymce.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(unique=True, max_length=30, error_messages={'unique': 'A user with that username already exists.'}, verbose_name='username', help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')])),
                ('first_name', models.CharField(verbose_name='first name', max_length=30, blank=True)),
                ('last_name', models.CharField(verbose_name='last name', max_length=30, blank=True)),
                ('email', models.EmailField(verbose_name='email address', max_length=254, blank=True)),
                ('is_staff', models.BooleanField(verbose_name='staff status', default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(verbose_name='active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('avatar', models.ImageField(default='avatar/default.png', max_length=200, null=True, verbose_name='用户头像', upload_to='avatar/%Y/%m', blank=True)),
                ('qq', models.CharField(verbose_name='QQ号码', max_length=20, null=True, blank=True)),
                ('mobile', models.CharField(verbose_name='手机号码', unique=True, max_length=11, null=True, blank=True)),
                ('groups', models.ManyToManyField(blank=True, verbose_name='groups', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(blank=True, verbose_name='user permissions', related_name='user_set', help_text='Specific permissions for this user.', related_query_name='user', to='auth.Permission')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'ordering': ['-id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='广告标题', max_length=50)),
                ('description', models.CharField(verbose_name='广告描述', max_length=200)),
                ('image_url', models.ImageField(verbose_name='图片路径', upload_to='avatar/%Y/%m')),
                ('callback_url', models.URLField(verbose_name='回调url', null=True, blank=True)),
                ('date_publish', models.DateTimeField(verbose_name='发布时间', auto_now_add=True)),
                ('index', models.IntegerField(verbose_name='排列顺序(从小到大)', default=999)),
            ],
            options={
                'verbose_name': '广告',
                'verbose_name_plural': '广告',
                'ordering': ['index', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='文章标题', max_length=50)),
                ('desc', models.CharField(verbose_name='文章描述', max_length=50)),
                ('content', tinymce.models.HTMLField(verbose_name='文章内容')),
                ('click_count', models.IntegerField(verbose_name='点击次数', default=0)),
                ('is_recommend', models.BooleanField(verbose_name='是否推荐', default=False)),
                ('date_publish', models.DateTimeField(verbose_name='发布时间', auto_now_add=True)),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'ordering': ['-date_publish'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='分类名称', max_length=30)),
                ('index', models.IntegerField(verbose_name='分类排名', default=999)),
            ],
            options={
                'verbose_name': '分类',
                'db_table': 'title_categort',
                'verbose_name_plural': '分类',
                'ordering': ['index', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('content', models.TextField(verbose_name='评论内容')),
                ('username', models.CharField(verbose_name='用户名', max_length=30, null=True, blank=True)),
                ('email', models.EmailField(verbose_name='邮箱地址', max_length=50, null=True, blank=True)),
                ('url', models.URLField(verbose_name='个人网页地址', max_length=100, null=True, blank=True)),
                ('date_publish', models.DateTimeField(verbose_name='发布时间', auto_now_add=True)),
                ('article', models.ForeignKey(null=True, verbose_name='文章', blank=True, to='blog.Article')),
                ('pid', models.ForeignKey(null=True, verbose_name='父级评论', blank=True, to='blog.Comment')),
                ('user', models.ForeignKey(null=True, verbose_name='用户', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='标题', max_length=50)),
                ('description', models.CharField(verbose_name='友情链接描述', max_length=200)),
                ('callback_url', models.URLField(verbose_name='url地址')),
                ('date_publish', models.DateTimeField(verbose_name='发布时间', auto_now_add=True)),
                ('index', models.IntegerField(verbose_name='排列顺序(从小到大)', default=999)),
            ],
            options={
                'verbose_name': '友情链接',
                'verbose_name_plural': '友情链接',
                'ordering': ['index', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='标签', max_length=40)),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
                'db_table': 'tag',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(verbose_name='分类', to='blog.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(verbose_name='标签', to='blog.Tag'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(verbose_name='用户', to=settings.AUTH_USER_MODEL),
        ),
    ]
