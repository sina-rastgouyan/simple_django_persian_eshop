# Generated by Django 4.1.3 on 2022-12-14 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0007_articlecomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlecomment',
            name='admin_confirm',
            field=models.BooleanField(default=False, verbose_name='تایید نهایی ادمین'),
        ),
    ]