# Generated by Django 3.2 on 2023-05-13 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_comment_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='review_id',
            new_name='review',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='title_id',
            new_name='title',
        ),
    ]
