# Generated by Django 4.2.15 on 2024-10-15 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EncryptDecrypt', '0005_alter_receive_complex_matrix_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='receive',
            name='decrypted_image',
            field=models.ImageField(blank=True, upload_to='decrypted_images/'),
        ),
    ]
