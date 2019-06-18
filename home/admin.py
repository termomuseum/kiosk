from django.contrib import admin
from home.models import GalleryEntry, GalleryEntryType, GalleryEntryCategory, GalleryEntryCategoryImage




# Register your models here.
admin.site.register(GalleryEntryCategory)
admin.site.register(GalleryEntryCategoryImage)
admin.site.register(GalleryEntryType)
admin.site.register(GalleryEntry)
