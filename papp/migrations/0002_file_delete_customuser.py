# Generated by Django 5.0 on 2023-12-24 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='file',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_file', models.FileField(upload_to='media/')),
            ],
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
