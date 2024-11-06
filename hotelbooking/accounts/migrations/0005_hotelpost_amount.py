# Generated by Django 5.1.3 on 2024-11-05 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_hotelpost_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelpost',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
