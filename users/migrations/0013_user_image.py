# Generated by Django 5.1 on 2024-09-01 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_menuitem_created_at_menuitem_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
