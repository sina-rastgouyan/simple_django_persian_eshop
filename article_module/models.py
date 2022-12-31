from django.db import models
from jalali_date import date2jalali

from account_module.models import User


# Create your models here.
class ArticleCategory(models.Model):
    parent = models.ForeignKey(
        'ArticleCategory',
        null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name='دسته بندی والد'
    )
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    url_title = models.CharField(max_length=200, unique=True, verbose_name='عنوان لینک دسته بندی')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی های مقاله'


class Article(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=400, db_index=True, allow_unicode=True, verbose_name='عنوان در url')
    short_description = models.TextField(max_length=400, verbose_name='توضیحات کوتاه')
    image = models.ImageField(upload_to='images/article_images')
    description = models.TextField(verbose_name='متن مقاله')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')
    selected_categories = models.ManyToManyField(ArticleCategory, verbose_name='دسته بندی ها')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='نویسنده', editable=False)
    create_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ ثبت')

    def get_jalali_create_date(self):
        return date2jalali(self.create_date)

    def get_jalali_create_time(self):
        return self.create_date.strftime('%H:%M')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='مقاله')
    parent = models.ForeignKey('ArticleComment', null=True, blank=True, on_delete=models.CASCADE, verbose_name='والد')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت نظر')
    text = models.TextField(verbose_name='متن نظر')

    # admin_confirm = models.BooleanField(default=False, verbose_name='تایید نهایی ادمین')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'نظر مقاله'
        verbose_name_plural = 'نظرات مقاله'
