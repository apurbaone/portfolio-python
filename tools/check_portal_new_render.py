import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','portfolio_site.settings')
import django
django.setup()
from django.test import Client
c=Client()
ok=c.login(username='mail@apurba.one',password='hayapurbathere')
print('login', ok)
r=c.get('/portal/new/')
print('status', r.status_code)
s=r.content.decode('utf-8')
print('has title input', 'id="id_title"' in s)
print('has banner input', 'name="banner_image"' in s)
print('snippet:', s[s.find('<form id="post-main-form"'):s.find('</form>', s.find('<form id="post-main-form"'))+7][:400].replace('\n',' '))
