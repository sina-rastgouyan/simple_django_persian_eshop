# Generated by Django 4.1.3 on 2022-12-13 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0005_remove_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='images/profile', verbose_name='تصویر شخص'),
        ),
    ]
