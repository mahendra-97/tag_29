# Generated by Django 4.1.5 on 2023-12-29 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag_api', '0017_alter_tagsmodel_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagsmodel',
            name='tag_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='tag_name'),
        ),
    ]