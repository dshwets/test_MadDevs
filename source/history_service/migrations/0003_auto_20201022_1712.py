# Generated by Django 2.2 on 2020-10-22 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history_service', '0002_commitshistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commitshistory',
            name='commit_json',
            field=models.TextField(verbose_name='Commit text'),
        ),
    ]
