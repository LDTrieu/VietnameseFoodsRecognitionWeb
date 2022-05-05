# Generated by Django 4.0.4 on 2022-05-02 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='searchResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('resultName', models.CharField(max_length=200)),
                ('url', models.URLField(max_length=250)),
                ('imageStatic', models.CharField(max_length=200)),
                ('accuracy', models.FloatField()),
            ],
        ),
    ]
