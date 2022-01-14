# Generated by Django 4.0.1 on 2022-01-13 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=22)),
                ('url', models.URLField()),
                ('source', models.CharField(max_length=200)),
                ('date', models.DateField(auto_now_add=True)),
                ('keywords', models.CharField(max_length=200)),
            ],
            options={
                'get_latest_by': 'date',
            },
        ),
    ]