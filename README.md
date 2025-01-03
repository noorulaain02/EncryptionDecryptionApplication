# Image Encryption and Decryption System

This project implements an **Image Encryption and Decryption System** that secures images by encrypting them using  Butterfly Algorithm for encryption and DES algorithm with XOR operation for key generations. The application is built using Django, OpenCV, and NumPy, providing functionalities such as encryption, decryption, key sharing, and user-friendly interaction.

---

## Features

### Encryption
- Encrypts an image using butterfly algortinm and the DES algorithm.
-  The user is provided with a secure encryption key, which must be shared via a separate communication medium.

### Decryption
- Decrypts the encrypted image using the same key.
- Displays the decrypted image upon successful key verification.

### Key Management
- Randomly generates an 16-character key for encryption.
- Provides options to copy the key and share it via external communication platforms like WhatsApp and email.

### Database Integration
- Stores the encrypted image, decryption key, and complex matrix (real and imaginary parts) in the database.
- Uses SQLite for data storage.

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
- **`EncryptDecrypt/`**: Contains the core logic of the app, including:
  - `admin.py`: Configuration for the Django admin interface.
  - `apps.py`: Application-specific settings.
  - `forms.py`: Custom forms used in the app.
  - `models.py`: Database models.
  - `urls.py`: URL patterns for the app.
  - `views.py`: The logic for handling requests and returning responses.
- **`ImageEncryptionDecryption/`**: Project-level configuration files.
  - `settings.py`: Global project settings.
  - `urls.py`: Root URL configurations for the project.
  - `wsgi.py`: WSGI configuration for deployment.
- **`media/`**: Stores dynamically generated files, such as uploaded, encrypted, and decrypted images.
- **`static/`**: Directory for static files collected for production use.
- **`templates/`**: Contains HTML files used for rendering views.
- **`db.sqlite3`**: SQLite database file storing application data.
- **`manage.py`**: Django’s command-line utility for administrative tasks.
- **`requirements.txt`**: Lists Python dependencies for the project.
- **`README.md`**: Documentation file explaining the project and how to use it.
  
## Known Issue
1. Debug Mode Deployment: Ensure DEBUG = False in production to avoid security risks.
2. SQLite Fetch Bug: May occur if the database is not configured properly for deployment.

## Note:
Use the encryption key responsibly and ensure secure sharing through trusted channels. This project is for educational purposes and is not recommended for critical security applications.

 #Contact
For questions or support, please contact:

- Email: noorulaain34ghazi@gmail.com
- GitHub: noorulaain02
