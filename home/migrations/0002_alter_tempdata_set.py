# Generated by Django 3.2.7 on 2021-09-06 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempdata',
            name='set',
            field=models.CharField(max_length=255),
        ),
    ]
