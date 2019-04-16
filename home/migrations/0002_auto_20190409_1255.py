# Generated by Django 2.1.7 on 2019-04-09 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryentry',
            name='entry_desc',
            field=models.TextField(default='', verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='galleryentry',
            name='entry_desc_full',
            field=models.TextField(default='', verbose_name='Full Description'),
        ),
        migrations.AddField(
            model_name='galleryentry',
            name='entry_file_url',
            field=models.FileField(default='', upload_to='', verbose_name='File'),
        ),
        migrations.AddField(
            model_name='galleryentry',
            name='entry_name',
            field=models.CharField(default='', max_length=100, verbose_name='Name'),
        ),
        migrations.AddField(
            model_name='galleryentry',
            name='entry_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.GalleryEntryType', verbose_name='Type'),
            preserve_default=False,
        ),
    ]