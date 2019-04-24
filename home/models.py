from django.db import models

# Model for Gallery Entry which describes an entry type
class GalleryEntryType(models.Model):
    type_name = models.CharField(max_length=40, verbose_name="Type")

    def __str__(self):
        return self.type_name


# Model which desctibes an entry
# TODO: Add entry_category
class GalleryEntry(models.Model):
    entry_type = models.ForeignKey(GalleryEntryType, on_delete=models.CASCADE, verbose_name="Type")
    entry_name = models.CharField(default="", max_length=100, verbose_name="Name")
    entry_file_url = models.FileField(default="", verbose_name="File")
    entry_desc = models.TextField(default="", verbose_name="Description")
    entry_desc_full = models.TextField(default="", verbose_name="Full Description")

    def __str__(self):
        return self.entry_name

