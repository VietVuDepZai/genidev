# Generated by Django 4.0.6 on 2022-10-10 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_alter_docs_video_iframe_alter_scratchdocs_iframe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scratchdocs',
            name='iframe',
            field=models.TextField(blank=True, null=True),
        ),
    ]
