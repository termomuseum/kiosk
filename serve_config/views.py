from os.path import join
from django.conf import settings
from django.http import HttpResponse
from .models import ConfigModel


def config(request):
  # default return value if config was not found
  content = 'ERR: no kiosk_config found.'
  
  # Getting a config from a database
  conf = None
  objects = ConfigModel.objects.filter(conf_name='kiosk_config')
  if len(objects) > 0:
    conf = objects[0]

  # if we've found a config object
  # we write the config text to content
  if conf != None: 
    content = conf.conf_text
    print(conf.conf_name + " requested and sent.")

  # returning content as plain text
  return HttpResponse(content=content, content_type='text/plain')

