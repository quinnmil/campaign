# Generated by Django 3.1 on 2020-11-11 06:07

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0007_auto_20201017_0058'),
    ]

    operations = [
        migrations.AddField(
            model_name='claimedjob',
            name='approved_by',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.PROTECT, to='accounts.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='claimedjob',
            name='completed_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 11, 11, 6, 7, 13, 447409, tzinfo=utc), verbose_name='Job completed on'),
            preserve_default=False,
        ),
    ]