from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.core.mail import get_connection
import logging

logger = logging.getLogger(__name__)

def send_external_email(subject, message, from_email, recipient_list):
    """
    Send email to external recipients with proper error handling
    """
    try:
        # Check if email settings are configured
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            raise Exception("Email credentials not configured. Please set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in your environment variables.")
        
        # Create email connection
        connection = get_connection(
            backend=settings.EMAIL_BACKEND,
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
            use_ssl=settings.EMAIL_USE_SSL,
        )
        
        # Create email message
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email or settings.DEFAULT_FROM_EMAIL,
            to=recipient_list,
            connection=connection,
        )
        
        # Send the email
        result = email.send()
        
        if result:
            logger.info(f"Email sent successfully to {recipient_list}")
            return True, "Email sent successfully"
        else:
            logger.error(f"Failed to send email to {recipient_list}")
            return False, "Failed to send email"
            
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Email sending error: {error_msg}")
        return False, error_msg

def test_email_connection():
    """
    Test the email connection settings
    """
    try:
        connection = get_connection(
            backend=settings.EMAIL_BACKEND,
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
            use_ssl=settings.EMAIL_USE_SSL,
        )
        connection.open()
        connection.close()
        return True, "Email connection successful"
    except Exception as e:
        return False, str(e)
