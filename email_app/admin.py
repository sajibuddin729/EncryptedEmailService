from django.contrib import admin
from .models import UserProfile, Email, Contact

admin.site.register(UserProfile)
admin.site.register(Email)
admin.site.register(Contact)
