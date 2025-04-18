from django.contrib import admin
from .models import User, Organizer, Campaign, Donation

# Register your models here.
admin.site.register(User)
admin.site.register(Organizer)
admin.site.register(Campaign)
admin.site.register(Donation)