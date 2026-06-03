# Bearer Token Auth API

A FastAPI-based authentication system demonstrating Bearer token (JWT) with a local login system. Users authenticate with credentials and receive a JWT to access protected endpoints.

## Endpoints

### 1. Root Endpoint

- **URL:** `/`
- **Method:** `GET`
- **Description:** Returns the service status.
- **Response:**
  ```json
  { "service": "Bearer Token Auth API", "status": "running" }
  ```

### 2. Login & Get Token

- **URL:** `/token`
- **Method:** `POST`
- **Description:** Authenticates a user and returns a Bearer JWT access token.
- **Request Body (form-data):**
  - `username`: (String) The username.
  - `password`: (String) The password.
- **Response:**
  ```json
  { "access_token": "eyJhbGci...", "token_type": "bearer" }
  ```
- **Error (invalid credentials):** `401 Unauthorized`

### 3. Get Current User

- **URL:** `/users/me/`
- **Method:** `GET`
- **Description:** Returns the authenticated user's profile.
- **Auth:** Requires a valid Bearer token in the `Authorization` header.
- **Response:**
  ```json
  { "username": "testuser", "email": "testuser@example.com", "full_name": "Test User", "disabled": false }
  ```

### 4. Access Protected Data

- **URL:** `/protected-data/`
- **Method:** `GET`
- **Description:** Returns a greeting message for the authenticated user, demonstrating protected resource access.
- **Auth:** Requires a valid Bearer token.
- **Response:**
  ```json
  { "message": "Hello testuser, you have access to protected data!" }
  ```

## Test Users

| Username   | Password      |
|------------|---------------|
| `testuser` | `testpassword`|
| `admin`    | `adminpassword`|

## Environment Variables

Create a `.env` file in the `Project_03/` directory:

```
SECRET_KEY="your-secret-key-here"
```

- `SECRET_KEY`: Used to sign JWT tokens. **Change this to a strong, random secret for production.**

An `.env.example` file is provided as a template.

## How to Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be accessible at `http://127.0.0.1:8000`. Visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI.
