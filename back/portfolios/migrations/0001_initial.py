<<<<<<< HEAD
# Generated by Django 4.2.16 on 2024-11-25 23:10
=======
# Generated by Django 4.2.16 on 2024-11-26 00:04
>>>>>>> 06ccb8c522d9933bf2d33e6a4d32446ed2b142fd

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< HEAD
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
=======
>>>>>>> 06ccb8c522d9933bf2d33e6a4d32446ed2b142fd
        ('contenttypes', '0002_remove_content_type_name'),
        ('finlife', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('total_investment', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('volatility', models.FloatField(blank=True, null=True)),
                ('predicted_economy', models.CharField(blank=True, choices=[('recession', '하락'), ('growth', '성장'), ('stability', '유지')], max_length=100, null=True)),
                ('risk_preference', models.CharField(blank=True, choices=[('low', '수비적'), ('medium', '보통'), ('high', '공격형')], max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('recommended_deposits', models.ManyToManyField(blank=True, related_name='recommended_to_portfolios', to='finlife.depositproducts')),
                ('recommended_savings', models.ManyToManyField(blank=True, related_name='recommended_to_portfolios', to='finlife.savingproducts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolios', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_step', models.PositiveIntegerField(default=0)),
                ('responses', models.JSONField(default=dict)),
                ('portfolio', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_response', to='portfolios.portfolio')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total_investment', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('quantity', models.DecimalField(decimal_places=6, editable=False, max_digits=15)),
                ('current_value', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('volatility', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='portfolios.portfolio')),
            ],
        ),
        migrations.CreateModel(
            name='RecommendationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('reason', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendation_logs', to='portfolios.portfolio')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Crypto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=10)),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total_investment', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('quantity', models.DecimalField(decimal_places=6, editable=False, max_digits=15)),
                ('current_value', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('volatility', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cryptocurrencies', to='portfolios.portfolio')),
            ],
        ),
    ]
