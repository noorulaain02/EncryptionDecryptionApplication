from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Image(models.Model):
    original_image = models.ImageField(upload_to='original_images/')
    preprocessed_image = models.ImageField(upload_to='preprocessed_images/', blank=True)
    gamma_corrected_image = models.ImageField(upload_to='gamma_corrected_images/', blank=True, null=True)
    encrypted_image = models.ImageField(upload_to='encrypted_images/', blank=True)
    complex_matrix = models.TextField(null=True, blank=True)  # For storing the complex matrix as JSON
    generated_key = models.TextField(default="")

    def __str__(self):
        return f"Image {self.id}"

class Send(models.Model):
    sender = models.ForeignKey(User, related_name='sent_images', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_images', on_delete=models.CASCADE)
    encrypted_image = models.ImageField(upload_to='sent_images/')  # Store the encrypted image
    complex_matrix = models.TextField(null=True, blank=True) # Store complex matrix as text (JSON serialized)
    sent_at = models.DateTimeField(auto_now_add=True)  # Record the time when the image was sent

    def __str__(self):
        return f"Image {self.id} "

class Receive(models.Model):
    sender = models.ForeignKey(User, related_name='images_sent_to_me', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='my_received_images', on_delete=models.CASCADE)
    encrypted_image = models.ImageField(upload_to='received_images/')
    complex_matrix = models.TextField(null=True, blank=True)  # Store complex matrix as text (JSON serialized)
    received_at = models.DateTimeField(default=timezone.now)
    decrypted_image = models.ImageField(upload_to='decrypted_images/', blank=True)


    def __str__(self):
        return f"Image {self.id} "
