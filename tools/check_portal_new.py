import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','portfolio_site.settings')
import django
django.setup()
from django.test import Client
c=Client()
ok = c.login(username='mail@apurba.one', password='hayapurbathere')
print('login', ok)
r = c.get('/portal/new/')
print('status', r.status_code)
s = r.content.decode('utf-8')
print('has_tinymce', 'tinymce.min.js' in s)
print('has_inline_input', 'id="inline-image-input"' in s)
print('has_gallery_input', 'id="gallery-input"' in s)
print('has_banner_input', 'name="banner_image"' in s)
print('snippet_preview:', s[:800].replace('\n',' '))
