# Generated by Django 5.1.5 on 2025-04-17 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('E_commerce', '0021_fooditem'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('image', models.ImageField(upload_to='device_images/')),
            ],
        ),
    ]
