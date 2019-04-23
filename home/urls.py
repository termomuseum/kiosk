from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('gallery_view/<int:gallery_item_id>/',
         views.gallery_view,
         name='gallery_view'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
