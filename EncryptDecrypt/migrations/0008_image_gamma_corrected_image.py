# Generated by Django 4.2.15 on 2024-10-24 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EncryptDecrypt', '0007_alter_receive_received_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='gamma_corrected_image',
            field=models.ImageField(blank=True, null=True, upload_to='gamma_corrected_images/'),
        ),
    ]
