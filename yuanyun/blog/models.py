from django.db import models
from django.contrib.auth.models import AbstractUser,python_2_unicode_compatible
# Create your models here.
from tinymce.models import HTMLField

@python_2_unicode_compatible
# 用户模型.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/.png', max_length=200, blank=True, null=True, verbose_name='用户头像')
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ号码')
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username


class TagManager(models.Manager):
    def get_tag(self):
        tag_name = []
        tag_list = self.values("name")
        for tag in tag_list:
            if tag['name'] not in tag_name:
                tag_name.append(tag['name'])
        return tag_name

#标签
@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=40,verbose_name='标签')
    objects = TagManager()
    class Meta:
        db_table = "tag"
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

#文章分类
@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=30,verbose_name="分类名称")
    index = models.IntegerField(default=999,verbose_name="分类排名")

    class Meta:
        db_table = "title_categort"
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.name



class ArticleManager(models.Manager):
    def get_date(self):
        article_date_list = []
        article_list = self.values("date_publish")
        for article_date in article_list:
            article_date = article_date["date_publish"].strftime('%Y%m 存档')
            if article_date not in article_date_list:
                article_date_list.append(article_date)
        return article_date_list
    def click_count(self):
        order_by = ('-click_count',)
        count_list = self.values("click_count").order_by(*order_by)
        article_click_list = []
        for count in count_list:
            article = Article.objects.filter('count=click_count')
            if article not in article_click_list:
                article_click_list.append(article)
        return article_click_list




# 文章模型
@python_2_unicode_compatible
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=50, verbose_name='文章描述')
    content = HTMLField(verbose_name='文章内容')
    click_count = models.IntegerField(default=0, verbose_name='浏览')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user=models.ForeignKey(User,verbose_name="用户")
    category = models.ForeignKey(Category,verbose_name='分类')
    tag = models.ManyToManyField(Tag,verbose_name="标签")


    objects = ArticleManager()

    class Meta:
        ordering = ['-date_publish']
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

# 评论模型
@python_2_unicode_compatible
class Comment(models.Model):
    content = HTMLField(verbose_name='评论内容')
    username = models.CharField(max_length=30, blank=True, null=True, verbose_name='用户名')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='邮箱地址')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='用户')
    article = models.ForeignKey(Article, blank=True, null=True, verbose_name='文章')
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)

# 友情链接
@python_2_unicode_compatible
class Links(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    description = models.CharField(max_length=200, verbose_name='友情链接描述')
    callback_url = models.URLField(verbose_name='url地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.title

# 广告
@python_2_unicode_compatible
class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name='广告标题')
    description = models.CharField(max_length=200,  verbose_name='广告描述')
    image_url = models.ImageField(upload_to='avatar/%Y/%m', verbose_name='图片路径')
    callback_url = models.URLField(null=True, blank=True, verbose_name='回调url')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = u'广告'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.title


