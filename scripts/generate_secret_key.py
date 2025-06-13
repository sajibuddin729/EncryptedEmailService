import secrets

# Generate a secure random secret key for Django
secret_key = secrets.token_urlsafe(50)
print(f"Generated Django Secret Key: {secret_key}")
print("\nAdd this to your .env file as:")
print(f"SECRET_KEY='{secret_key}'")
