# Generated by Django 4.0.6 on 2022-10-10 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parents', '0004_remove_parents_student_model_parents_student_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parents',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
