# Generated by Django 3.1 on 2020-09-10 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_listing_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='image',
            field=models.URLField(default='https://en.wikipedia.org/wiki/File:No_image_available.svg'),
        ),
    ]
