# Generated by Django 3.1.3 on 2020-12-06 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20201206_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='is_active',
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.AlterField(
            model_name='offercategory',
            name='image',
            field=models.ImageField(upload_to='C:\\Users\\pe6ka\\VisualStudioCodeProjects\\Python_web\\bidster\\bidster\\media\\categories'),
        ),
    ]
