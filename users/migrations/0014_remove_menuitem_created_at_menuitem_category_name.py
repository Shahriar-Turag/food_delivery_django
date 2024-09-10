# Generated by Django 5.1 on 2024-09-02 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_user_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='created_at',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='category_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
