import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','portfolio_site.settings')
import django
django.setup()
from django.test import Client
from blog.models import Post

c = Client()
if not c.login(username='mail@apurba.one', password='hayapurbathere'):
    print('login failed')
    raise SystemExit(1)

data = {
    'title': 'Test Post 123',
    'slug': 'test-post-123',
    'excerpt': 'testing',
    'body': 'This is a test body.'
}
resp = c.post('/portal/new/', data, follow=True)
print('post status code:', resp.status_code)
# print redirect chain
print('redirects:', resp.redirect_chain)
# check if post exists
exists = Post.objects.filter(slug='test-post-123').exists()
print('post exists:', exists)
if exists:
    p = Post.objects.get(slug='test-post-123')
    print('post id/title:', p.pk, p.title, 'published:', p.published)
# if form errors were displayed in response, show a small snippet
s = resp.content.decode('utf-8')
if 'Form errors' in s or 'Please fix the errors' in s:
    print('response contains form errors snippet:')
    start = s.find('Form errors')
    print(s[start:start+300])
else:
    print('no form errors shown in response')
