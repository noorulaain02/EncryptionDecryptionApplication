# Image Encryption and Decryption System

This project implements an **Image Encryption and Decryption System** that secures images by encrypting them using the DES algorithm with XOR operations and a user-provided key. The application is built using Django, OpenCV, and NumPy, providing functionalities such as encryption, decryption, key sharing, and user-friendly interaction.

---

## Features

### Encryption
- Encrypts an image using the DES algorithm with XOR and Fourier Transform.
- The user is provided with a secure encryption key, which must be shared via a separate communication medium.

### Decryption
- Decrypts the encrypted image using the same key.
- Displays the decrypted image upon successful key verification.

### Key Management
- Randomly generates an 8-character ASCII key for encryption.
- Provides options to copy the key and share it via external communication platforms like WhatsApp and email.

### Database Integration
- Stores the encrypted image, decryption key, and complex matrix (real and imaginary parts) in the database.
- Uses SQLite for data storage.

### Web Interface
- Provides an intuitive web interface for users to upload images, perform encryption, and decrypt images.
- Displays messages for errors like invalid keys or missing data.

---

## Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Libraries**: OpenCV, NumPy
- **Database**: SQLite
- **Deployment**: Gunicorn (for production), Python's built-in server (for development)

---

## Installation and Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)


1. Clone the repository:
   ```bash
   git clone https://github.com/noorulaain02/image-encryption-decryption.git
   cd image-encryption-decryption

2. Install Dependencies
   ```bash
   pip install -r requirements.txt

3. Run Database Migrations
   ```bash
   python manage.py makemigrations
   python manage.py migrate

4. Start the server
   ```bash
   python manage.py runserver

5. Access the application at http://127.0.0.1:8000/.

## Directory Structure
-`ImageEncryptionDecryption/`
   - `EncryptDecrypt/` contains your Django app logic, including templates, models, views, and static assets.
        - `admin.py`
        - `apps.py`
        - `forms.py`
        - `models.py`
        - `urls.py`
        - `views.py`
   - `ImageEncryptionDecryption/`
        - `settings.py`
        - `urls.py`
        - `wsgi.py`
   - `media/` is used to store dynamically generated files such as encrypted, decrypted, and uploaded images.
   - `static/` is for collected static files used in production.
   - `templates/` 
   - `db.sqlite3` is the database file.
   - `manage.py` is the Django management script.
   - `requirements.txt` lists all the dependencies.
   - `README.md` is your project description file.
     
## Known Issue
1. Debug Mode Deployment: Ensure DEBUG = False in production to avoid security risks.
2. SQLite Fetch Bug: May occur if the database is not configured properly for deployment.

## Note:
Use the encryption key responsibly and ensure secure sharing through trusted channels. This project is for educational purposes and is not recommended for critical security applications.

📧 #Contact
For questions or support, please contact:

- Email: noorulaain34ghazi@gmail.com
- GitHub: noorulaain02
