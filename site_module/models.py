from django.db import models


# Create your models here.

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=250, verbose_name='نام سایت')
    site_url = models.CharField(max_length=250, verbose_name='دامنه سایت')
    address = models.CharField(max_length=250, verbose_name='آدرس')
    site_phone = models.CharField(max_length=250, null=True, blank=True, verbose_name='تلفن')
    site_fax = models.CharField(max_length=250, null=True, blank=True, verbose_name='فکس')
    site_email = models.CharField(max_length=250, null=True, blank=True, verbose_name='ایمیل')
    copy_right = models.TextField(verbose_name='متن کپی رایت سایت')
    about_us = models.TextField(verbose_name='متن درباره ما')
    site_logo = models.ImageField(upload_to='images/site_settings/site_logo', max_length=250, verbose_name='لوگو سایت')
    is_main_settings = models.BooleanField(max_length=250, verbose_name='تنظیمات اصلی')

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'


class FooterLinkBox(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'دسته بندی لینک های فوتر'
        verbose_name_plural = 'دسته بندی های لینک های فوتر'

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.URLField(max_length=650, verbose_name='لینک')
    footer_link_box = models.ForeignKey(to=FooterLinkBox, on_delete=models.CASCADE, verbose_name='دسته بندی')

    class Meta:
        verbose_name = 'لینک فوتر'
        verbose_name_plural = 'لینک های فوتر'

    def __str__(self):
        return self.title


class Slider(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات اسلایدر')
    url_title = models.CharField(max_length=100, verbose_name='عنوان لینک')
    url = models.URLField(max_length=650, verbose_name='آدرس لینک')
    image = models.ImageField(upload_to='images/slider_images')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدر ها'

    def __str__(self):
        return self.title


class SiteBanner(models.Model):
    class SiteBannerPositions(models.TextChoices):
        product_list = 'product_list', 'صفحه لیست محصولات'
        product_detail = 'product_detail', 'صفحه جزئیات محصولات'

    title = models.CharField(max_length=200, verbose_name='عنوان بنر')
    url = models.URLField(max_length=400, verbose_name='آدرس بنر', null=True, blank=True)
    image = models.ImageField(upload_to='images/banners', verbose_name='تصویر بنر')
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال')
    position = models.CharField(max_length=200, choices=SiteBannerPositions.choices, verbose_name='جایگاه نمایش بنر')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بنر تبلیغاتی'
        verbose_name_plural = 'بنر های تبلیغاتی'
