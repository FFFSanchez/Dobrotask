# Generated by Django 4.2.4 on 2023-09-03 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_tasksubtask_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=180, unique=True, verbose_name='Название категории'),
        ),
    ]
