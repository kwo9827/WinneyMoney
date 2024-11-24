from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0001_initial'),  # 이전 마이그레이션 파일
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='risk_preference',
            field=models.IntegerField(null=True),
        ),
    ]
