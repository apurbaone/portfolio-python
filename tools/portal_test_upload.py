import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
import django
django.setup()
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

c = Client()
ok = c.login(username='mail@apurba.one', password='hayapurbathere')
print('logged in:', ok)
url = reverse('portal:upload_image')
img = SimpleUploadedFile('test.png', b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR', content_type='image/png')
r = c.post(url, {'image': img})
print('status', r.status_code)
try:
    print('json', r.json())
except Exception as e:
    print('response_text', r.content.decode('utf-8'))
