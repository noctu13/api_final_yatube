# Generated by Django 3.0.7 on 2020-06-11 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20200611_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления'),
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=set(),
        ),
    ]
