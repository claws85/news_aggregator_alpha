# Generated by Django 4.0.1 on 2022-01-14 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_aggregator_alpha', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
