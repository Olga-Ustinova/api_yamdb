# Generated by Django 3.2 on 2023-05-13 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20230513_1520'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('username',)},
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default='user', max_length=9),
        ),
    ]
