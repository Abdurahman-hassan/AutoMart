from django.core.asgi import get_asgi_application
from octos.base import get_settings_module

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", get_settings_module())

application = get_asgi_application()
