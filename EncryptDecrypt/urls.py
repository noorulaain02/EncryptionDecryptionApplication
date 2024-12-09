from django.contrib import admin
from django.urls import path
from EncryptDecrypt import views
from django.conf.urls.static import static
from ImageEncryptionDecryption import settings
from .views import upload_image, preprocess_image,decryption_page

urlpatterns = [
    path('', views.login_view, name='login'),  # Default page is the login page
    path('home/', views.home, name='home'),  # Home page after login
    path('register/', views.register, name='register'),  # Registration page
    path('logout/', views.logout_view, name='logout'),  # Logout page
    path("about",views.about,name='about'),
    path("contact",views.contact,name='contact'),
    path('home/upload/', upload_image, name='upload_image'),
    path('encrypt_image/<int:image_id>/', views.encrypt_image, name='encrypt_image'),
   path('encrypt_image/<int:image_id>/', views.encrypt_image, name='encrypt_image'),
    path('preprocess/<int:image_id>/', views.preprocess_image, name='preprocess_image'),
    
   path('encrypt_image/<int:image_id>/', views.encrypt_image, name='encrypt_image'),
    path('send/<int:image_id>/', views.send_page, name='send_page'),
    path('send_image/<int:image_id>/', views.send_encrypted_image, name='send_encrypted_image'),

    path('send_encrypted/<int:image_id>/', views.send_encrypted_image, name='send_encrypted_image'),
    path('received_images/', views.received_images, name='received_images'),
    path('receive/<int:send_id>/', views.receive_image, name='receive_image'),
    path('decryption_page/<int:image_id>/', views.decryption_page, name='decryption_page'),
    path('home/decrypt/', views.decryption_page, name='decryption_page'),  # Without image_id
    path('delete/<int:image_id>/', views.delete_received_image, name='delete_received_image'),
    path('encrypt/<int:image_id>/send/', views.send_page, name='send_page'),
    path('encrypt_image/<int:image_id>/send_image.html/', views.send_page, name='send_page'),

    path('encrypt_image/<int:image_id>/send/', views.send_page, name='send_page'),
    path('view_received/<int:image_id>/', views.view_received_image, name='view_received_image'),
    path('final_image/<int:image_id>/', views.decrypt_image, name='decrypt_image'),
    #path('encrypt/<int:image_id>/', views.encrypt_image, name='encrypt'),  # Function to encrypt the image
    #path('send/<int:image_id>/', views.send_encrypted_image, name='send_encrypted_image'),
    path('receive_images/', views.receive_image, name='receive_images'),
    path('gamma_correction/<int:image_id>/', views.gamma_correction_page, name='gamma_correction_page'),

    # URL for applying gamma correction (AJAX request)
    path('apply_gamma_correction/', views.apply_gamma_correction, name='apply_gamma_correction'),
    path('save_adjusted_image/<int:image_id>/', views.save_adjusted_image, name='save_adjusted_image'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
