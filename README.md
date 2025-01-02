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

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/image-encryption-decryption.git
   cd image-encryption-decryption
