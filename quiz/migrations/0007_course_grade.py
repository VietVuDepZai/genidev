# Generated by Django 4.0.6 on 2022-10-01 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0008_teacher_class_model_teacher_grade'),
        ('quiz', '0006_course_atempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='grade',
            field=models.ManyToManyField(to='teacher.teacher'),
        ),
    ]
