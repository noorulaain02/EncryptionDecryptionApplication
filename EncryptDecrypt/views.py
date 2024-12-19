from EncryptDecrypt.models import Image
from EncryptDecrypt.forms import ImageUploadForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
import numpy as np
from .models import Image
import cv2
import os
import matplotlib.pyplot as plt
import json 
import socket
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SendImageForm
from .models import Image, Send  # Assuming your models are Image and Send
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Image, Send  # Assuming these models exist
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings  # To use settings.MEDIA_ROOT for image paths
from .models import Send, Receive
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import ImageUploadForm
from .models import Image

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')  # Render your home page template

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('login')

def index(request):
    return render(request,'home.html')

def about(request):
        return HttpResponse("This is About Page")


def encrypt(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('some_view')  # Change 'some_view' to the name of your next view
    else:
        form = ImageUploadForm()
    return render(request, 'encrypt.html', {'form': form})


def contact(request):
        return HttpResponse("This is Contact Page")

from django.core.exceptions import ValidationError

def upload_image(request):
    uploaded_image_url = None
    image_id = None
    error_message = None  # Variable to store the error message

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if the uploaded file is a GIF
            file_extension = request.FILES['original_image'].name.split('.')[-1].lower()
            if file_extension == 'gif':
                error_message = "GIFs are not allowed. Please upload an image in JPG or PNG format."
            else:
                image_instance = form.save()
                uploaded_image_url = image_instance.original_image.url
                image_id = image_instance.id
    else:
        form = ImageUploadForm()

    return render(request, 'upload_image.html', {
        'form': form,
        'uploaded_image_url': uploaded_image_url,
        'image_id': image_id,
        'error_message': error_message
    })

"""
def upload_image(request):
    uploaded_image_url = None
    image_id = None
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            uploaded_image_url = image_instance.original_image.url
            image_id = image_instance.id
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form, 'uploaded_image_url': uploaded_image_url, 'image_id': image_id})
"""
def preprocess_image(request, image_id):
    image_instance = get_object_or_404(Image, id=image_id)
    image_path = image_instance.original_image.path

    # Image preprocessing function
    def image_preprocessing(image_path):
        image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resized_image = cv2.resize(gray_image, (400, 400))
        rotated_image = cv2.warpAffine(resized_image, cv2.getRotationMatrix2D((128, 128), 0, 1.0), (400, 400))
        decision = np.mean(rotated_image)
        gamma = 0.4 if decision < 100 else 1.8 if decision > 150 else 1
        gamma_corrected_image = np.array(255 * (rotated_image / 255) ** gamma, dtype=np.uint8)
        return gamma_corrected_image

    preprocessed_image = image_preprocessing(image_path)

    # Create the preprocessed_images directory if it doesn't exist
    preprocessed_image_dir = os.path.join(settings.MEDIA_ROOT, 'preprocessed_images')
    if not os.path.exists(preprocessed_image_dir):
        os.makedirs(preprocessed_image_dir)

    preprocessed_image_path = os.path.join(preprocessed_image_dir, f"{image_id}_preprocessed.jpg")
    cv2.imwrite(preprocessed_image_path, preprocessed_image)

    # Save the preprocessed image path to the database
    image_instance.preprocessed_image = f"preprocessed_images/{image_id}_preprocessed.jpg"
    image_instance.save()

    # Add 'image_id' to the context
    context = {
        'preprocessed_image_url': image_instance.preprocessed_image.url,
        'image_id': image_id,  # Add image_id to the context
    }

    return render(request, 'preprocess.html', context)

import random
import string
'''
def encrypt_image(request, image_id):
    image_instance = get_object_or_404(Image, id=image_id)
    image_path = image_instance.preprocessed_image.path

    # Generate a random 8-character ASCII key
    key1 = ''.join(random.choices(string.ascii_letters + string.digits, k=8)).encode('ascii')

    # Encryption function
    def image_des(image_path, key):
        image1 = cv2.imread(image_path)
        key_array = np.frombuffer(key, dtype=np.uint8)  # Convert key to uint8 array
        key_repeated = np.tile(key_array, image1.size // len(key_array))
        image_uint8 = image1.astype(np.uint8)
        mixed_image = np.bitwise_xor(image_uint8.flatten(), key_repeated).reshape(image1.shape)
        encry = np.fft.fft2(mixed_image)  # Using FFT as a placeholder
        return encry

    encrypted_image = image_des(image_path, key1)

    # Save encrypted image to media directory
    encrypted_image_dir = os.path.join(settings.MEDIA_ROOT, 'encrypted_images')
    if not os.path.exists(encrypted_image_dir):
        os.makedirs(encrypted_image_dir)

    encrypted_image_path = os.path.join(encrypted_image_dir, f"{image_id}_encrypted.jpg")

    real_image = np.real(encrypted_image)
    image_uint8 = np.uint8(real_image)

    cv2.imwrite(encrypted_image_path, image_uint8)

    # Store complex matrix (real + imaginary) as JSON for future decryption
    real_part = encrypted_image.real.tolist()
    imag_part = encrypted_image.imag.tolist()

    complex_data = {
        'real': real_part,
        'imag': imag_part
    }

    # Save the complex matrix JSON and encrypted image path to the database
    image_instance.complex_matrix = json.dumps(complex_data)
    image_instance.encrypted_image = f"encrypted_images/{image_id}_encrypted.jpg"
    image_instance.save()

    # Pass encrypted image URL and ASCII key to the template
    return render(request, 'encrypt.html', {
        'encrypt_image_url': image_instance.encrypted_image.url,
        'encryption_key': key1.decode('ascii')  # Pass key as ASCII string
    })



'''
def encrypt_image(request, image_id):
    image_instance = get_object_or_404(Image, id=image_id)
    
    image_path = image_instance.preprocessed_image.path

    # Function to perform encryption
    def image_des(image_path,key):
        image1 = cv2.imread(image_path)
        key_array = np.frombuffer(key, dtype=np.uint8)  # Convert key to uint8 array
        key_repeated = np.tile(key_array, image1.size // len(key_array))
        image_uint8 = image1.astype(np.uint8)
        mixed_image = np.bitwise_xor(image_uint8.flatten(), key_repeated).reshape(image1.shape)
        encry =  np.fft.fft2(mixed_image)  # Example using FFT as a placeholde
        return encry

    key1 = os.urandom(8)
    encrypted_image = image_des(image_path,key1)

    # Save encrypted image to media directory
    encrypted_image_dir = os.path.join(settings.MEDIA_ROOT, 'encrypted_images')
    if not os.path.exists(encrypted_image_dir):
        os.makedirs(encrypted_image_dir)

    encrypted_image_path = os.path.join(encrypted_image_dir, f"{image_id}_encrypted.jpg")

    real_image = np.real(encrypted_image)
    image_uint8 = np.uint8(real_image)  # or np.uint8(real_image)

    cv2.imwrite(encrypted_image_path, image_uint8)

       # Store complex matrix (real + imaginary) as JSON for future decryption
    real_part = encrypted_image.real.tolist()
    imag_part = encrypted_image.imag.tolist()

    complex_data = {
        'real': real_part,
        'imag': imag_part
    }
    
    # Save the complex matrix JSON to the database
    image_instance.complex_matrix = json.dumps(complex_data)
    image_instance.encrypted_image = f"encrypted_images/{image_id}_encrypted.jpg"
    image_instance.save()

    # Pass encrypted image URL to the template
    return render(request, 'encrypt.html', {'encrypt_image_url': image_instance.encrypted_image.url,'encryption_key': key1.hex()})

from django.contrib import messages
from django.shortcuts import redirect

def send_encrypted_image(request, image_id):
    image = Image.objects.get(id=image_id)

    if request.method == 'POST':
        receiver_username = request.POST.get('receiver')
        
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect('send_page', image_id=image_id)

        # Store the sent image and complex matrix in the 'Send' table
        Send.objects.create(
            sender=request.user,
            receiver=receiver,
            encrypted_image=image.encrypted_image,
            complex_matrix=image.complex_matrix
        )
        
        messages.success(request, f"Image sent to {receiver_username} successfully!")
        return redirect('send_page', image_id=image_id)
    else:
        messages.error(request, "Invalid request method")
        return redirect('send_page', image_id=image_id)

'''
def send_encrypted_image(request, image_id):
    image = Image.objects.get(id=image_id)

    if request.method == 'POST':
        receiver_username = request.POST.get('receiver')
        image = Image.objects.get(id=image_id)
        
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return HttpResponse("User does not exist", status=404)
        
        # Store the sent image and complex matrix in the 'Send' table
        Send.objects.create(
            sender=request.user,
            receiver=receiver,
            encrypted_image=image.encrypted_image,
            complex_matrix=image.complex_matrix
        )
        
        return HttpResponse(f"Image sent to {receiver_username} successfully!")
    else:
        return HttpResponse("Invalid request method", status=400)
'''
def send_page(request, image_id):
    return render(request, 'send.html', {'image_id': image_id})

@login_required
def received_images(request):
    received_images_list = Send.objects.filter(receiver=request.user)
    return render(request, 'received_images.html', {'received_images_list': received_images_list})


@login_required
def receive_image(request, send_id):
    try:
        sent_image = Send.objects.get(id=send_id, receiver=request.user)
        
        # Create a new entry in the Receive table
        Receive.objects.create(
            sender=sent_image.sender,
            receiver=sent_image.receiver,
            encrypted_image=sent_image.encrypted_image,
            complex_matrix=sent_image.complex_matrix,
            received_at=timezone.now() 
        )

        return redirect('decryption_page')  # Redirect to the decryption page after receiving

    except Send.DoesNotExist:
        return redirect('received_images')  # If the sent image is not found or is not for the user


from django.shortcuts import render, get_object_or_404, redirect
from .models import Send, Receive

# View to handle displaying the received image and the "Decrypt" button
def view_received_image(request, image_id):
    received_image = get_object_or_404(Receive, id=image_id)
    return render(request, 'view_received.html', {'received_image': received_image})

@login_required
def decryption_page(request):
    # Fetch all received images for the logged-in user
    received_images = Receive.objects.filter(receiver=request.user)
    
    # Pass the received images to the template
    return render(request, 'decryption_page.html', {'received_images': received_images})
'''
def decrypt_image(request, image_id):
    image_instance = get_object_or_404(Receive, id=image_id)

    if image_instance.complex_matrix is None:
        return render(request, 'home.html', {'message': 'No complex matrix found for this image.'})

    try:
        complex_data = json.loads(image_instance.complex_matrix)
    except json.JSONDecodeError:
        return render(request, 'home.html', {'message': 'Invalid complex matrix data.'})

    real_part = np.array(complex_data['real'])
    imag_part = np.array(complex_data['imag'])
    complex_matrix = real_part + 1j * imag_part

    def revert_key_from_image(mixed_image, key):
        key_array = np.frombuffer(key, dtype=np.uint8)
        key_repeated = np.tile(key_array, mixed_image.size // len(key_array))
        mixed_image_uint8 = mixed_image.astype(np.uint8)
        original_image = np.bitwise_xor(mixed_image_uint8.flatten(), key_repeated).reshape(mixed_image.shape)
        return original_image

    def apply_inverse_butterfly_encryption(complex_matrix):
        return np.fft.ifft2(complex_matrix)

    if request.method == 'POST':
        user_input_key = request.POST.get('encryption_key', '').encode('ascii')

        if len(user_input_key) != 8:
            return render(request, 'decrypt_image.html', {'error': 'The key must be exactly 8 ASCII characters.'})

        ifft_image = apply_inverse_butterfly_encryption(complex_matrix)
        ifft_image_uint8 = np.abs(ifft_image).astype(np.uint8)
        decrypted_image = revert_key_from_image(ifft_image_uint8, user_input_key)

        decrypted_image_dir = os.path.join(settings.MEDIA_ROOT, 'decrypted_images')
        if not os.path.exists(decrypted_image_dir):
            os.makedirs(decrypted_image_dir)

        decrypted_image_path = os.path.join(decrypted_image_dir, f"{image_id}_decrypted.jpg")
        cv2.imwrite(decrypted_image_path, decrypted_image)

        return render(request, 'decrypt_image.html', {
            'decrypted_image_url': f"{settings.MEDIA_URL}decrypted_images/{image_id}_decrypted.jpg"
        })

    return render(request, 'decrypt_image.html', {'image_instance': image_instance})

'''
def decrypt_image(request, image_id):
    # Get the image instance from the database using the image ID
    image_instance = get_object_or_404(Receive, id=image_id)

    if image_instance.complex_matrix is None:
        return render(request, 'home.html', {'message': 'No complex matrix found for this image.'})

    # Load the complex matrix from the database
    try:
        complex_data = json.loads(image_instance.complex_matrix)
    except json.JSONDecodeError:
        return render(request, 'home.html', {'message': 'Invalid complex matrix data.'})

    # Proceed with decryption...
    real_part = np.array(complex_data['real'])
    imag_part = np.array(complex_data['imag'])
    complex_matrix = real_part + 1j * imag_part

    # Function to revert the key from the mixed encrypted image using XOR
    def revert_key_from_image(mixed_image, key):
        key_array = np.frombuffer(key, dtype=np.uint8)  # Convert key to uint8 array

        # Repeat the key to match the size of the image
        key_repeated = np.tile(key_array, mixed_image.size // len(key_array))

        # Ensure mixed_image is in uint8 format
        mixed_image_uint8 = mixed_image.astype(np.uint8)

        # Apply XOR operation to get the original image back
        original_image = np.bitwise_xor(mixed_image_uint8.flatten(), key_repeated).reshape(mixed_image.shape)
        return original_image

    # Function to apply inverse butterfly encryption (using IFFT)
    def apply_inverse_butterfly_encryption(complex_matrix):
        return np.fft.ifft2(complex_matrix)  # Apply Inverse FFT
    
    # Retrieve user-provided decryption key from POST request
    if request.method == 'POST':
        user_input_key_hex = request.POST.get('encryption_key', '')
        
        # Convert the provided key from hex to bytes
        try:
            user_input_key = bytes.fromhex(user_input_key_hex)
        except ValueError:
            return render(request, 'decrypt_image.html', {'error': 'Invalid key format. Please enter a valid key.'})
        
        # Ensure the key is exactly 8 bytes
        if len(user_input_key) != 8:
            return render(request, 'decrypt_image.html', {'error': 'The key must be exactly 8 bytes.'})
        
        # Apply Inverse FFT (Butterfly decryption)
        ifft_image = apply_inverse_butterfly_encryption(complex_matrix)
        
        # Convert the IFFT result to uint8 format for further processing
        ifft_image_uint8 = np.abs(ifft_image).astype(np.uint8)
        
        # Revert the XOR operation using the provided key to get the original image
        decrypted_image = revert_key_from_image(ifft_image_uint8, user_input_key)
        
        # Save the decrypted image to the media directory
        decrypted_image_dir = os.path.join(settings.MEDIA_ROOT, 'decrypted_images')
        if not os.path.exists(decrypted_image_dir):
            os.makedirs(decrypted_image_dir)

        decrypted_image_path = os.path.join(decrypted_image_dir, f"{image_id}_decrypted.jpg")
        
        # Save the decrypted image
        cv2.imwrite(decrypted_image_path, decrypted_image)
        
        return render(request, 'decrypt_image.html', {
        'decrypted_image_url': f"{settings.MEDIA_URL}decrypted_images/{image_id}_decrypted.jpg"
    })
 
    return render(request, 'decrypt_image.html', {'image_instance': image_instance})


@login_required
def delete_received_image(request, image_id):
    image_instance = get_object_or_404(Receive, id=image_id)
    
    # Delete the image instance
    image_instance.delete()
    
    # Redirect back to the decryption page (assuming it's named 'decryption_page')
    return redirect('decryption_page')
import numpy as np
from PIL import Image
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from io import BytesIO
import base64
from .models import Image

@login_required
def gamma_correction_page(request, image_id):
    # Fetch the preprocessed image from the database
    image_obj = get_object_or_404(Image, id=image_id)
    image_url = image_obj.preprocessed_image.url

    return render(request, 'gamma_correction.html', {'image_url': image_url, 'image_id': image_id})

@login_required
def apply_gamma_correction(request):
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        gamma_value = float(request.POST.get('gamma_value'))

        # Fetch the preprocessed image
        image_obj = get_object_or_404(Image, id=image_id)
        image = Image.open(image_obj.preprocessed_image.path)

        # Apply gamma correction
        gamma_corrected_image = gamma_correction(image, gamma_value)

        # Save the gamma-corrected image
        corrected_image_buffer = BytesIO()
        gamma_corrected_image.save(corrected_image_buffer, format='PNG')
        image_obj.gamma_corrected_image.save(f"gamma_corrected_{image_obj.id}.png", corrected_image_buffer)
        image_obj.save()

        # Convert the gamma-corrected image to base64 for display
        buffered = BytesIO()
        gamma_corrected_image.save(buffered, format="PNG")
        corrected_image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        corrected_image_data = f"data:image/png;base64,{corrected_image_base64}"

        return JsonResponse({'success': True, 'corrected_image': corrected_image_data})
    return JsonResponse({'success': False})

def gamma_correction(image, gamma):
    inv_gamma = 1.0 / gamma
    lut = [((i / 255.0) ** inv_gamma) * 255 for i in range(256)]
    return image.point(lut)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import base64

@csrf_exempt  # Only use csrf_exempt if absolutely necessary; better to handle CSRF properly
def save_adjusted_image(request, image_id):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']

        # Assuming you have a model called Image with a field `gamma_corrected_image`
        try:
            image_instance = Image.objects.get(id=image_id)
            image_instance.gamma_corrected_image.save(image_file.name, image_file)

            return JsonResponse({'success': True})
        except Image.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Image not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request.'})
