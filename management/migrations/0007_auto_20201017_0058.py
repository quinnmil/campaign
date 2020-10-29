# Generated by Django 3.1 on 2020-10-17 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_auto_20200928_0548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claimedjob',
            name='status',
            field=models.CharField(choices=[('P', 'In Progress'), ('C', 'Completed'), ('Q', 'Quit'), ('R', 'Rejected'), ('S', 'Submitted')], default='P', max_length=1, verbose_name='job status'),
        ),
    ]