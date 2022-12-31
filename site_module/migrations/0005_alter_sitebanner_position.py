# Generated by Django 4.1.3 on 2022-12-18 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0004_sitebanner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitebanner',
            name='position',
            field=models.CharField(choices=[('product_list', 'صفحه لیست محصولات'), ('product_detail', 'صفحه جزئیات محصولات'), ('about_us', 'صفحه درباره ما')], max_length=200, verbose_name='جایگاه نمایش بنر'),
        ),
    ]