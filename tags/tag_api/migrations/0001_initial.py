# Generated by Django 4.1.5 on 2023-12-27 04:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TagsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('tag_name', models.CharField(max_length=255, unique=True, verbose_name='tag_name')),
                ('scope', models.CharField(blank=True, max_length=255, verbose_name='scope')),
            ],
            options={
                'verbose_name': 'tags',
                'db_table': 'tags',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='VM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vm_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('vm_name', models.CharField(max_length=255, unique=True, verbose_name='vm_name')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation_date')),
                ('tags', models.ManyToManyField(related_name='vms', to='tag_api.tagsmodel')),
            ],
            options={
                'verbose_name': 'vms',
                'db_table': 'vms',
                'managed': True,
            },
        ),
    ]