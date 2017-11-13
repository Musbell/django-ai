# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-30 02:18
from __future__ import unicode_literals
import numpy as np

from django.db import migrations, models
from django.conf import settings


def populate_visits(apps, schema_editor):
    UserInfo = apps.get_model("examples", "UserInfo")
    # Use a fixed seed for generate content
    np.random.seed(123456)
    # Size of table
    table_size = getattr(settings, "DJANGO_AI_EXAMPLES_USERINFO_SIZE", 200)
    # Floor'ed Normal around a 100 for total page visits
    visits_pages = np.floor(np.random.normal(100, 5, size=(table_size,)))
    # and around 40% of them are in pages of type A
    visits_pages_a = np.floor(np.random.normal(40, 2, size=(table_size,)))

    uis = UserInfo.objects.all()
    # Update the objects in the Model
    for index, ui in enumerate(uis):
        ui.visits_pages = visits_pages[index]
        ui.visits_pages_a = visits_pages_a[index]
        ui.save(update_fields=['visits_pages', 'visits_pages_a'])


def unpopulate_visits(apps, schema_editor):
    """
    This is for making the migration reversible, it doesn't do anything
    because the fields will be removed after by the reverse of AddField.
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('examples', '0007_userinfo_cluster_1'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='visits_pages_a',
            field=models.IntegerField(
                default=1, verbose_name='Visits on Pages A'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='visits_pages',
            field=models.IntegerField(
                default=1, verbose_name='Visits on Pages (Total)'),
            preserve_default=False,
        ),
        migrations.RunPython(populate_visits,
                             unpopulate_visits),
    ]