# HackerJr API

This API provides functionalities for steganography (embedding and extracting encrypted messages in images) and extracting metadata from images.

## Endpoints

### 1. Root Endpoint

- **URL:** `/`
- **Method:** `GET`
- **Description:** Returns the status of the service. Useful if you need to check if the API is running, by pinging it.
- **Response Example:**
  ```/dev/null/example.json
  {
    "service": "exploit image metadata",
    "status": "running"
  }
  ```

### 2. Encrypt Data into Image

- **URL:** `/encrypt`
- **Method:** `POST`
- **Description:** Encrypts a given message and embeds it into an uploaded image. The API returns a ZIP file containing the modified image and the encryption key required for decryption.
- **Request Body (multipart/form-data):**
  - `file`: (File) The image file to embed the message into. Must be an image type.
  - `message`: (String) The message to encrypt and embed.
- **Response:** A `.zip` file containing `encrypted.png` and `key.txt`.

### 3. Decrypt Data from Image

- **URL:** `/decrypt`
- **Method:** `POST`
- **Description:** Extracts hidden data from an uploaded image and decrypts it using the provided encryption key.
- **Request Body (multipart/form-data):**
  - `file`: (File) The image file containing the hidden message.
  - `key`: (String) The encryption key obtained during the encryption process.
- **Response Example (on success):**
  ```/dev/null/example.json
  {
    "message": "Your decrypted message here"
  }
  ```
- **Error Response Example (Incorrect key or corrupted image):**
  ```/dev/null/example.json
  {
    "detail": "Incorrect key or corrupted image"
  }
  ```

### 4. Extract Image Metadata

- **URL:** `/extract`
- **Method:** `POST`
- **Description:** Extracts various metadata, including EXIF data, GPS information, and file details from an uploaded image.
- **Request Body (multipart/form-data):**
  - `file`: (File) The image file to extract metadata from. Must be an image type.
- **Response Example:**
  ```/dev/null/example.json
  {
    "filename": "my_image.jpg",
    "content_type": "image/jpeg",
    "image": {
      "width": 1920,
      "height": 1080,
      "format": "JPEG",
      "mode": "RGB"
    },
    "file": {
      "size_bytes": 123456,
      "sha256": "a1b2c3d4e5f6..."
    },
    "gps": {
      "latitude": 34.052235,
      "longitude": -118.243683
    },
    "metadata": {
      "Make": "Canon",
      "Model": "Canon EOS 5D Mark IV",
      "DateTimeOriginal": "2023:10:27 10:30:00"
      // ... other EXIF data
    }
  }
  ```

## Environment Variables

This project uses environment variables, managed with `python-dotenv`, for sensitive configurations. You need to create a `.env` file in the root directory of the project.

### `.env` File Setup

1.  Create a file named `.env` in the `Project_01/` directory.
2.  Add the following variable to the `.env` file:

    ```/dev/null/.env
    MAGIC="YOUR_CUSTOM_MAGIC_STRING"
    ```

    -   `MAGIC`: A custom flag used to identify the embedded schematic within images. It defaults to "D3C0D3" if not set. **It is highly recommended to change this to a unique, secret string for production environments.**

## How to Run the API

To run the HackerJr API, follow these steps:

1.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    (Assuming `requirements.txt` exists and contains all necessary packages like `fastapi`, `uvicorn`, `Pillow`, `python-dotenv`, `cryptography`)

2.  **Run the Application:**

    ```bash
    uvicorn main:app --reload
    ```

    This will start the FastAPI application, typically accessible at `http://127.0.0.1:8000`.
