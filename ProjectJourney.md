🗺️ Project Setup & Backend Foundation — Step-by-Step
✅ Step 1 — Initialize the Project with uv

Created a new Python project using:

uv init

This generated the base project structure and dependency system.

✅ Step 2 — Create Virtual Environment

Created and activated a virtual environment using:

uv venv

Ensured dependency isolation and clean package management for the project.

✅ Step 3 — Modify main.py & Add API Route

Updated main.py to:

Initialize the FastAPI application.

Create the first route endpoint for testing or health checks.

This served as the starting backend entry point for the system.

✅ Step 4 — Create config/ Folder

Added a new folder named config.

Purpose: centralize configuration-related logic (database, environment variables, etc.).

✅ Step 5 — Add MongoDB Configuration File

Inside config/, created a database module to:

Load environment variables using python-dotenv.

Read:

MongoDB connection URI.

Database name.

Initialize MongoDB client.

Test connection using ping.

Create database object.

Fetch the users collection for future authentication logic.

👉 This established the database layer for the project.

✅ Step 6 — Setup MongoDB Cloud Project

Created a MongoDB Atlas account.

Set up a new cloud database project.

Generated:

Database cluster.

Connection URI.

Added credentials to environment variables instead of hard-coding them.

✅ Step 7 — Add .env File

Created a .env file to securely store:

MONGODB_URI

MONGO_DB_NAME

Ensured secrets remain outside version control.

✅ Step 8 — Add requirements.txt

Added initial dependencies:

pymongo → MongoDB driver.

fastapi[standard] → backend framework.

uvicorn → ASGI server for running FastAPI apps.
✅ Step 9 — Create auth/ Module

Added a dedicated auth folder to isolate authentication and authorization logic from the main application.

This follows a modular backend design pattern.

✅ Step 10 — Implement Password Hashing Logic

Created a hashpasswords.py file to handle secure credential storage:

Used bcrypt for cryptographic hashing.

Implemented:

hash_password() → converts plaintext password into a salted hash.

verify_password() → checks login attempts against stored hashes.

Applied:

UTF-8 encoding before hashing.

Decoding hashed output to string for MongoDB storage.

👉 This ensures:
✔ Passwords are never stored in plaintext
✔ Secure authentication practices
✔ Industry-standard cryptography

✅ Step 11 — Define User Signup Schema

Created a Pydantic model for request validation:

SignUpRequest

username

password

role

This enforces:

Proper request body structure.

Automatic validation by FastAPI.

✅ Step 12 — Create Authentication Routes

Added a routes.py file inside auth/ to expose authentication endpoints.

Implemented:
🔹 Signup Endpoint (POST /signup)

Checks if the username already exists.

Hashes the password before storing it.

Inserts user record into MongoDB.

Returns success confirmation.

🔹 Login Flow with HTTP Basic Auth

Used FastAPI’s HTTPBasic security dependency.

Created an authenticate() function to:

Fetch user from MongoDB.

Validate password using bcrypt.

Reject invalid users or credentials with HTTP 401.

Added:

GET /login route protected by the authentication dependency.

Returns user role and welcome message on success.

✅ Step 13 — Database Integration for Auth

Connected authentication logic directly to:

users_collection from MongoDB config.

This made the database the single source of truth for users.