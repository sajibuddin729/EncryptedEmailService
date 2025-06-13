import os
import secrets

# Generate a sample .env file for the project
secret_key = secrets.token_urlsafe(50)

env_content = f"""# Django settings
SECRET_KEY='{secret_key}'
DEBUG=True

# Email settings
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='your-email@gmail.com'
EMAIL_HOST_PASSWORD='your-app-password'
"""

print("Sample .env file content:")
print("------------------------")
print(env_content)
print("------------------------")
print("\nCreate a .env file in your project root with the above content.")
print("Replace the email settings with your actual SMTP server details.")
print("\nFor Gmail, you'll need to use an App Password instead of your regular password.")
print("Learn more: https://support.google.com/accounts/answer/185833")
