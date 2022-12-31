from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify

from account_module.models import User


# Create your models here.

class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان دسته بندی')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    def __str__(self):
        return f"({self.title} - {self.url_title})"

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ProductBrand(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='نام برند')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='نام در url')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان محصول')
    brand = models.ForeignKey(ProductBrand, verbose_name='برند محصول', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ManyToManyField(ProductCategory, related_name='product_categories', verbose_name='دسته بندی ها')
    image = models.ImageField(
        upload_to='images/products',
        null=True, blank=True,
        verbose_name='تصویر محصول'
    )
    price = models.IntegerField(verbose_name='قیمت')
    short_description = models.CharField(max_length=360, null=True, db_index=True, verbose_name='توضیحات کوتاه')
    description = models.TextField(db_index=True, verbose_name='توضیحات اصلی')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    slug = models.SlugField(
        default="", null=False,
        db_index=True,
        max_length=200,
        unique=True,
        verbose_name='عنوان در url'
    )
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class ProductTag(models.Model):
    caption = models.CharField(max_length=230, db_index=True, verbose_name='عنوان تگ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ ها'


class ProductVisit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=40, verbose_name='آی پی')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='کاربر')

    def __str__(self):
        return f"{self.product.title} / {self.ip}"

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدید های محصول'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product_gallery', verbose_name='تصویر')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'