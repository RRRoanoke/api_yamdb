# Generated by Django 3.2 on 2023-02-05 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='comment',
            name='unique review1',
        ),
        migrations.AddConstraint(
            model_name='comment',
            constraint=models.UniqueConstraint(fields=('author',), name='unique review1'),
        ),
    ]
