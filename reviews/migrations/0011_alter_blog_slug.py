# Generated by Django 4.1.7 on 2023-07-17 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0010_alter_blog_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='slug'),
        ),
    ]