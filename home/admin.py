from django.contrib import admin
from home.models import GalleryEntry, GalleryEntryType

# Register your models here.
admin.site.register(GalleryEntryType)
admin.site.register(GalleryEntry)
