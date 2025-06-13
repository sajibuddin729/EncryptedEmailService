# 🔐 Encrypted Email Service

A Django-based end-to-end encrypted email service that ensures only intended recipients can read your messages. Built with modern web technologies and strong encryption standards.


## ✨ Features

- **🔒 End-to-End Encryption**: Messages are encrypted with RSA-2048 encryption
- **🔑 Automatic Key Management**: Public/private key pairs generated automatically
- **📧 Hybrid Email Support**: Send encrypted emails to registered users and plain emails to external recipients
- **📱 Responsive Design**: Mobile-friendly interface built with Bootstrap 5
- **👥 Contact Management**: Manage your contacts and their public keys
- **🔍 Email Threading**: Organized inbox and sent items
- **⚙️ SMTP Integration**: Connect with existing email providers
- **🛡️ Secure Authentication**: Django's built-in authentication system

## 🏗️ Architecture

### Encryption Flow
1. **Registration**: Each user gets a unique RSA key pair (2048-bit)
2. **Sending**: Messages are encrypted with recipient's public key
3. **Storage**: Only encrypted content is stored in the database
4. **Reading**: Messages are decrypted with recipient's private key

### Security Features
- RSA-2048 encryption for message content
- Secure key generation using Python's cryptography library
- CSRF protection for all forms
- Session-based authentication
- Secure password hashing

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   \`\`\`bash
   git clone https://github.com/yourusername/encrypted-email-service.git
   cd encrypted-email-service
   \`\`\`

2. **Create a virtual environment**
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   \`\`\`

3. **Install dependencies**
   \`\`\`bash
   pip install django django-crispy-forms crispy-bootstrap5 cryptography python-dotenv
   \`\`\`

4. **Set up environment variables**
   \`\`\`bash
   python scripts/setup_env_variables.py
   \`\`\`

5. **Edit the .env file** with your email credentials:
   \`\`\`env
   SECRET_KEY='your-generated-secret-key'
   DEBUG=True
   
   # Email Configuration
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=your-email@gmail.com
   \`\`\`

6. **Apply database migrations**
   \`\`\`bash
   cd encrypted_email
   python manage.py makemigrations email_app
   python manage.py migrate
   \`\`\`

7. **Create a superuser**
   \`\`\`bash
   python manage.py createsuperuser
   \`\`\`

8. **Run the development server**
   \`\`\`bash
   python manage.py runserver
   \`\`\`

9. **Access the application**
   Open your browser and go to \`http://127.0.0.1:8000/\`

## ⚙️ Configuration

### Email Provider Setup

#### Gmail Configuration
1. Enable 2-factor authentication on your Google account
2. Go to [Google Account Settings](https://myaccount.google.com/)
3. Security → App passwords
4. Generate a new app password for "Mail"
5. Use the 16-character app password in \`EMAIL_HOST_PASSWORD\`

#### Other Email Providers
- **Outlook**: \`smtp-mail.outlook.com:587\` (TLS)
- **Yahoo**: \`smtp.mail.yahoo.com:587\` (TLS)
- **Custom SMTP**: Configure your own SMTP server settings

### Testing Email Configuration

\`\`\`bash
python manage.py test_email --to recipient@example.com
\`\`\`

### Development Mode (No SMTP)

For testing without SMTP setup, uncomment this line in \`settings.py\`:

\`\`\`python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
\`\`\`

## 📖 Usage Guide

### 1. User Registration
- Navigate to the registration page
- Create an account with username, email, and password
- A public/private key pair is automatically generated

### 2. Sending Encrypted Emails
- Click "Compose" to create a new email
- Enter recipient's email address
- Write your message
- **Internal recipients**: Messages are automatically encrypted
- **External recipients**: Messages are sent as plain text with a warning

### 3. Reading Emails
- **Inbox**: View received encrypted emails
- **Sent**: View your sent emails
- Messages are automatically decrypted when opened

### 4. Managing Contacts
- Add contacts with their email addresses
- Optionally add their public keys for external encryption
- View contact list with encryption status

### 5. Profile Settings
- View your public key
- Configure email provider settings
- Check email connection status

## 🔧 API Reference

### Models

#### User Profile
- Stores user's public/private key pair
- Email provider configuration

#### Email
- Encrypted email content
- Sender and recipient information
- Timestamp and read status

#### External Recipient
- Tracks emails sent to non-registered users

#### Contact
- User's contact list
- Public key storage for external contacts

### Key Functions

#### Encryption/Decryption
\`\`\`python
from email_app.utils import encrypt_message, decrypt_message

# Encrypt a message
encrypted = encrypt_message("Hello World", recipient_public_key)

# Decrypt a message
decrypted = decrypt_message(encrypted_content, private_key)
\`\`\`

#### Email Sending
\`\`\`python
from email_app.email_utils import send_external_email

success, message = send_external_email(
    subject="Test Email",
    message="Hello World",
    from_email="sender@example.com",
    recipient_list=["recipient@example.com"]
)
\`\`\`


### Running Tests

\`\`\`bash
python manage.py test
\`\`\`

### Database Migrations

\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

### Custom Management Commands

\`\`\`bash
# Test email configuration
python manage.py test_email --to recipient@example.com
\`\`\`

## 🔒 Security Considerations

### Encryption Details
- **Algorithm**: RSA with OAEP padding
- **Key Size**: 2048 bits
- **Hashing**: SHA-256
- **Message Chunking**: Large messages are split into chunks for RSA encryption

### Security Best Practices
- Private keys are stored securely in the database
- CSRF protection on all forms
- Session-based authentication
- Secure password hashing with Django's built-in system
- Environment variables for sensitive configuration

### Limitations
- **RSA Message Size**: Limited by key size (190 bytes per chunk for RSA-2048)
- **Server-Side Decryption**: Private keys are accessible to the server
- **External Recipients**: Messages to non-registered users are not encrypted

### Recommendations for Production
- Use HTTPS in production
- Implement client-side encryption/decryption
- Add two-factor authentication
- Regular security audits
- Backup encryption keys securely

## 🚨 Troubleshooting

### Common Issues

#### CSRF Verification Failed
- Ensure \`{% csrf_token %}\` is in all forms
- Check that CSRF middleware is enabled
- Clear browser cookies and cache

#### Email Connection Errors
- Verify SMTP settings in \`.env\` file
- Check firewall and network connectivity
- For Gmail, use App Password, not regular password
- Test with: \`python manage.py test_email\`

#### Multiple Users with Same Email
- The system handles this by using the first matching user
- Consider adding unique constraints in production

#### Encryption/Decryption Errors
- Ensure both users have valid key pairs
- Check that public keys are properly formatted
- Verify message size limits

### Debug Mode

Enable debug output by setting \`DEBUG=True\` in settings.py. This will show:
- Email configuration details
- Detailed error messages
- SQL queries (in development)

### Logs

Check Django logs for detailed error information:
\`\`\`bash
tail -f django.log
\`\`\`

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (\`git checkout -b feature/amazing-feature\`)
3. Commit your changes (\`git commit -m 'Add amazing feature'\`)
4. Push to the branch (\`git push origin feature/amazing-feature\`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Ensure security best practices

## 🗺️ Roadmap

### Planned Features
- [ ] Client-side encryption/decryption
- [ ] File attachment support with encryption
- [ ] Two-factor authentication
- [ ] Email threading and conversations
- [ ] Mobile app (React Native)
- [ ] PGP key import/export
- [ ] Email scheduling
- [ ] Advanced search functionality
- [ ] Email templates
- [ ] Bulk email operations

### Performance Improvements
- [ ] Database query optimization
- [ ] Caching implementation
- [ ] Async email sending
- [ ] Message compression


## 📊 Statistics

- **Lines of Code**: ~2,000+
- **Languages**: Python, HTML, CSS, JavaScript
- **Dependencies**: Django, Bootstrap, Cryptography
- **Database**: SQLite (development), PostgreSQL (production ready)

---

Made by [Md. Sajib Uddin] for academic purposes 
