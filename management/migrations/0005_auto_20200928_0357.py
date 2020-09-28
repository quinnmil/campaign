# Generated by Django 3.1 on 2020-09-28 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_auto_20200919_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claimedjob',
            name='status',
            field=models.CharField(choices=[('P', 'In Progress'), ('C', 'Completed'), ('Q', 'Quit'), ('R', 'R'), ('S', 'S')], default='P', max_length=1, verbose_name='job status'),
        ),
    ]