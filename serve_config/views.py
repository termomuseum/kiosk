from os.path import join
from django.conf import settings
from django.http import HttpResponse
from .models import ConfigModel


def index(request):
  content = 'Hello, Kiosk!'
  return HttpResponse(content=content, content_type='text/plain')


def config(request):
  content = 'ERR: no kiosk_config found.'
  
  conf = ''
  objects = ConfigModel.objects.filter(conf_name='kiosk_config')
  if len(objects) > 0:
    conf = objects[0]

  if conf != '': 
    content = conf.conf_text
    print(conf.conf_name)
    print(conf.conf_text)

  return HttpResponse(content=content, content_type='text/plain')
