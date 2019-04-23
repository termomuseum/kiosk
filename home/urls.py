from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('view_video/<int:gallery_item_id>/',
         views.gallery_view_video,
         name='gallery_view_video'),
    path('temp/', views.temp, name='temp')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
