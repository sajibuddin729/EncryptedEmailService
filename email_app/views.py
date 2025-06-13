from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from .models import Email, Contact, UserProfile, ExternalRecipient
from .forms import UserRegistrationForm, EmailForm, ContactForm, UserProfileForm
from .utils import generate_key_pair, encrypt_message, decrypt_message
from .email_utils import send_external_email, test_email_connection

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Generate key pair for the new user
            public_key, private_key = generate_key_pair()
            
            # Save keys to user profile
            profile = user.profile
            profile.public_key = public_key
            profile.private_key = private_key
            profile.save()
            
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def inbox(request):
    received_emails = Email.objects.filter(recipients=request.user).order_by('-date_sent')
    return render(request, 'email_app/inbox.html', {'emails': received_emails})

@login_required
def sent(request):
    sent_emails = Email.objects.filter(sender=request.user).order_by('-date_sent')
    return render(request, 'email_app/sent.html', {'emails': sent_emails})

@login_required
def compose(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient_email = form.cleaned_data['recipient_email']
            
            # Create email but don't save yet
            email = form.save(commit=False)
            email.sender = request.user
            
            # Check if recipient is in the system
            # Use filter() instead of get() to handle multiple users with same email
            recipients = User.objects.filter(email=recipient_email)
            
            if recipients.exists():
                # If multiple users have the same email, use the first one
                recipient = recipients.first()
                
                # Encrypt the message with recipient's public key
                try:
                    recipient_public_key = recipient.profile.public_key
                    if not recipient_public_key:
                        messages.warning(request, "Recipient doesn't have a public key. Sending unencrypted.")
                        email.encrypted_content = form.cleaned_data['encrypted_content']
                    else:
                        plain_content = form.cleaned_data['encrypted_content']
                        email.encrypted_content = encrypt_message(plain_content, recipient_public_key)
                    
                    email.save()
                    email.recipients.add(recipient)
                    
                    messages.success(request, 'Email sent successfully!')
                    return redirect('inbox')
                except Exception as e:
                    messages.error(request, f'Encryption error: {str(e)}')
            else:
                # Handle external recipient
                try:
                    # Save as unencrypted for external recipients
                    email.encrypted_content = form.cleaned_data['encrypted_content']
                    email.is_external = True
                    email.save()
                    
                    # Create external recipient record
                    external_recipient = ExternalRecipient.objects.create(
                        email=recipient_email,
                        email_reference=email
                    )
                    
                    # Send via SMTP to the actual external address
                    success, error_message = send_external_email(
                        subject=email.subject,
                        message=email.encrypted_content,
                        from_email=request.user.email,
                        recipient_list=[recipient_email]
                    )
                    
                    if success:
                        messages.success(request, f'Email sent to external recipient {recipient_email}. Note: External emails are not encrypted end-to-end.')
                    else:
                        messages.warning(request, f'Email saved but could not be delivered: {error_message}')
                    
                    return redirect('inbox')
                except Exception as e:
                    messages.error(request, f'Error sending to external recipient: {str(e)}')
    else:
        form = EmailForm()
    
    return render(request, 'email_app/compose.html', {'form': form})

@login_required
def view_email(request, email_id):
    email = get_object_or_404(Email, id=email_id)
    
    # Check if user is authorized to view this email
    if request.user != email.sender and not email.recipients.filter(id=request.user.id).exists():
        messages.error(request, "You don't have permission to view this email.")
        return redirect('inbox')
    
    # Mark as read if user is a recipient
    if email.recipients.filter(id=request.user.id).exists() and not email.read:
        email.read = True
        email.save()
    
    # Decrypt the message if user is a recipient
    decrypted_content = None
    if request.user in email.recipients.all():
        try:
            private_key = request.user.profile.private_key
            decrypted_content = decrypt_message(email.encrypted_content, private_key)
        except Exception as e:
            messages.error(request, f'Decryption error: {str(e)}')
            decrypted_content = "Error decrypting message."
    elif request.user == email.sender and email.is_external:
        # If sender is viewing an external email, show the original content
        decrypted_content = email.encrypted_content
    
    context = {
        'email': email,
        'decrypted_content': decrypted_content,
    }
    
    return render(request, 'email_app/view_email.html', context)

@login_required
def contacts(request):
    user_contacts = Contact.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, 'Contact added successfully!')
            return redirect('contacts')
    else:
        form = ContactForm()
    
    return render(request, 'email_app/contacts.html', {
        'contacts': user_contacts,
        'form': form
    })

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    # Test email connection
    connection_status = None
    if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
        success, message = test_email_connection()
        connection_status = {'success': success, 'message': message}
    
    return render(request, 'email_app/profile.html', {
        'form': form,
        'public_key': request.user.profile.public_key,
        'connection_status': connection_status
    })
