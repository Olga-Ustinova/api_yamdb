# Generated by Django 3.2 on 2023-05-14 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_review_unique_title_user_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genretitle',
            old_name='genre_id',
            new_name='genre',
        ),
        migrations.RenameField(
            model_name='genretitle',
            old_name='title_id',
            new_name='title',
        ),
    ]
