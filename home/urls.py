from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    # Home view
    path('', views.index, name='index'),
    # Gallery item view
    path('gallery_view/<int:gallery_item_id>/',
         views.gallery_view,
         name='gallery_view'),

    # + static... is added to allow media files to 
    # be accessed by user or views
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
