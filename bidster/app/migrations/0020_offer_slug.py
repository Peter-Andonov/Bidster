# Generated by Django 3.1.3 on 2020-12-12 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20201212_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='slug',
            field=models.SlugField(default='offer', editable=False),
            preserve_default=False,
        ),
    ]
