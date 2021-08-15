# Generated by Django 3.2.6 on 2021-08-15 11:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20210815_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 15, 11, 47, 1, 569550)),
        ),
        migrations.AddConstraint(
            model_name='todoitem',
            constraint=models.UniqueConstraint(fields=('title', 'todo_list'), name='name of constraint'),
        ),
    ]