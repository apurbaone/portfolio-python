import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','portfolio_site.settings')
import django
django.setup()
from django.test import Client
c=Client()
r=c.get('/admin/')
print('status', r.status_code)
s=r.content.decode('utf-8')
print('has_portal_badge', 'portal v2' in s)
print('has_brand', 'Apurba.one' in s)
