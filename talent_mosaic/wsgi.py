import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talent_mosaic.settings')
application = get_wsgi_application()
