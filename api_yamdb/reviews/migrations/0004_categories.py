# Generated by Django 3.2 on 2023-02-10 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20230209_2242'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
    ]
