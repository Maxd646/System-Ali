# Generated by Django 5.1.6 on 2025-02-18 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('E_commerce', '0008_remove_food_category_food_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_email', models.EmailField(max_length=254)),
                ('food_item', models.CharField(max_length=255)),
                ('quantity', models.PositiveIntegerField()),
                ('delivery_address', models.TextField()),
                ('phone_number', models.CharField(max_length=15)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
