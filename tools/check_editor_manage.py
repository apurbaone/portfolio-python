import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

c = Client()
if not c.login(username='mail@apurba.one', password='hayapurbathere'):
    print('login failed')
    raise SystemExit(1)
r = c.get('/portal/new/')
s = r.content.decode('utf-8')
print('status', r.status_code)
print('has_editor_div', '<div id="editor"' in s)
print('has_toolbar', 'id="editor-toolbar"' in s)
print('has_fallback_note', 'Editor not found: TinyMCE missing' in s)
start = s.find('<div id="editor-toolbar"')
if start!=-1:
    end = s.find('</div>', start)
    print(s[start:end+6])
