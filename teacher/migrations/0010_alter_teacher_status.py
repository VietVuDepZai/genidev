# Generated by Django 4.0.6 on 2022-10-02 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0009_alter_teacher_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]