# Generated by Django 2.2.7 on 2019-11-15 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0004_recipe_preparation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
        ),
    ]