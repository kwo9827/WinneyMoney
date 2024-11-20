# Generated by Django 4.2.16 on 2024-11-20 06:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finlife', '0002_alter_depositproducts_join_deny'),
    ]

    operations = [
        migrations.AddField(
            model_name='depositproducts',
            name='favorited_by',
            field=models.ManyToManyField(related_name='favorited_deposit_products', through='finlife.UserFavoriteProducts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='depositproducts',
            name='join_deny',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='userfavoriteproducts',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorites', to=settings.AUTH_USER_MODEL),
        ),
    ]
