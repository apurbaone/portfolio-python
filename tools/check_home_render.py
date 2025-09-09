import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','portfolio_site.settings')
import django
django.setup()
from django.test import Client
c = Client()
r = c.get('/')
s = r.content.decode('utf-8')
print('status', r.status_code)
print('has latest-card', 'latest-card' in s)
start = s.find('<section class="latest-posts')
end = s.find('</section>', start)
print('snippet:', s[start:end+10].replace('\n',' ')[:400])
