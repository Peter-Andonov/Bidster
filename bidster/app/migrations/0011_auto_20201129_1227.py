# Generated by Django 3.1.3 on 2020-11-29 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20201129_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='highest_bid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.bid'),
        ),
    ]