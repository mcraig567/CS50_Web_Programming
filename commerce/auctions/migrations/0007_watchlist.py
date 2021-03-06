# Generated by Django 3.1 on 2020-09-09 00:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_listing_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watched', to='auctions.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watching', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
