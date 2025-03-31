# Generated by Django 5.1.7 on 2025-03-31 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_activitylog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='streak',
        ),
        migrations.AddField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, help_text='More details about you, your skills, or interests.'),
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, help_text='A short bio about yourself.', max_length=150),
        ),
        migrations.AddField(
            model_name='user',
            name='github_link',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='linkedin_link',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile_pics/default.png', null=True, upload_to='profile_pics/'),
        ),
        migrations.AddField(
            model_name='user',
            name='tags',
            field=models.CharField(blank=True, help_text='Comma-separated tags (e.g., Python, Django, Learner)', max_length=200),
        ),
        migrations.AddField(
            model_name='user',
            name='website_link',
            field=models.URLField(blank=True),
        ),
        migrations.DeleteModel(
            name='ActivityLog',
        ),
    ]
