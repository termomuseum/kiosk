from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from . import views

app_name = 'home'
urlpatterns = [
    # Home view
    path('', views.index, name='index'),
    path('category/', views.index, name='category_view'),
    re_path('category/(?P<pk>\d+)', views.gallery_category, name='category_view'),
    re_path('gallery_video/(?P<pk>\d+)', views.gallery_video, name='video'),
    path('gallery_video/', views.gallery_video, name='video_view'),
    re_path('gallery_image/(?P<pk>\d+)/',views.gallery_image,name='image'),
    path('gallery_image/',views.gallery_image,name='image_view'),
    re_path('gallery_presentation/(?P<pk>\d+)/',views.gallery_presentation,name='presentation'),
    path('gallery_presentation/',views.gallery_presentation,name='presentation_view'),

    # + static... is added to allow media files to 
    # be accessed by user or views
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
