# Generated by Django 4.0.3 on 2022-04-06 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_mooyahouser_disabled_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mooyahouser',
            name='disabled_reason',
            field=models.TextField(null=True, verbose_name='탈퇴 사유'),
        ),
    ]