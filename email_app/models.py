from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    public_key = models.TextField(blank=True, null=True)
    private_key = models.TextField(blank=True, null=True)
    email_provider = models.CharField(max_length=100, blank=True, null=True)
    email_password = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Email(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_emails')
    recipients = models.ManyToManyField(User, related_name='received_emails')
    subject = models.CharField(max_length=255)
    encrypted_content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    is_external = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_sent']
    
    def __str__(self):
        return f"{self.subject} - {self.sender.username}"

class ExternalRecipient(models.Model):
    email = models.EmailField()
    email_reference = models.ForeignKey(Email, on_delete=models.CASCADE, related_name='external_recipients')
    
    def __str__(self):
        return self.email

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    contact_email = models.EmailField()
    contact_name = models.CharField(max_length=100)
    public_key = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('user', 'contact_email')
    
    def __str__(self):
        return f"{self.contact_name} ({self.contact_email})"
