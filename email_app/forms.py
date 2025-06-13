from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Email, Contact, UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class EmailForm(forms.ModelForm):
    recipient_email = forms.EmailField(label='To')
    
    class Meta:
        model = Email
        fields = ['recipient_email', 'subject', 'encrypted_content']
        widgets = {
            'encrypted_content': forms.Textarea(attrs={'rows': 10}),
        }
        labels = {
            'encrypted_content': 'Message',
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['contact_name', 'contact_email', 'public_key']
        widgets = {
            'public_key': forms.Textarea(attrs={'rows': 5}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email_provider', 'email_password']
        widgets = {
            'email_password': forms.PasswordInput(),
        }
