# Generated by Django 4.0.6 on 2022-07-19 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='category',
            field=models.CharField(blank=True, choices=[('Furniture', 'Furni'), ('IT Equipment', 'IT Equipment'), ('Phone', 'Phone'), ('Electronic', 'Electronic')], max_length=50, null=True),
        ),
    ]
