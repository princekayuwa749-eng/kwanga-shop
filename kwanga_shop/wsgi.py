"""
WSGI config for kwanga_shop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import sys

# Chemin vers ton projet Django
path = '/home/kwangashop/kwanga_shop'
if path not in sys.path:
    sys.path.append(path)

# Définit le module de configuration Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'kwanga_shop.settings'

# Active Django via WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()