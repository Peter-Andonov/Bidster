# Generated by Django 3.1.3 on 2020-11-14 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20201114_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='offercategory',
            name='image',
            field=models.ImageField(default=1, upload_to='C:\\Users\\pe6ka\\VisualStudioCodeProjects\\Python_web\\bidster\\bidster\\media\\categories'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]