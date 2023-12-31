# Generated by Django 3.2.9 on 2023-08-20 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0004_auto_20230819_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='blog_picture',
            field=models.ImageField(default='user_auth/default_images/default-blog-image.png', upload_to='blog_pics/'),
        ),
        migrations.AddField(
            model_name='blog',
            name='draft',
            field=models.BooleanField(default=False),
        ),
    ]
