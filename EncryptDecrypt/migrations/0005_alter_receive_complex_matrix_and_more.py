# Generated by Django 4.2.15 on 2024-10-14 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EncryptDecrypt', '0004_image_generated_key_alter_image_encrypted_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receive',
            name='complex_matrix',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='send',
            name='complex_matrix',
            field=models.TextField(blank=True, null=True),
        ),
    ]
