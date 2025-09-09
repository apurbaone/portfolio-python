from django.db import models
from django.urls import reverse


class Post(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)
	excerpt = models.TextField(blank=True)
	# legacy path field (kept for compatibility). Prefer using banner_image for uploads.
	image = models.CharField(max_length=255, blank=True, help_text='Path under static/, e.g. blog/images/post1.jpg')
	banner_image = models.ImageField(upload_to='blog/banners/', blank=True, null=True)
	body = models.TextField()
	published = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-published']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post_detail', args=[self.slug])

	def excerpt_preview(self, length=180):
		if self.excerpt:
			return self.excerpt
		return (self.body[:length] + '...') if len(self.body) > length else self.body


class PostImage(models.Model):
	post = models.ForeignKey(Post, related_name='gallery', on_delete=models.CASCADE)
	image = models.ImageField(upload_to='blog/gallery/')
	thumbnail = models.ImageField(upload_to='blog/gallery/thumbs/', blank=True, null=True)
	caption = models.CharField(max_length=255, blank=True)

	def __str__(self):
		return f"Image for {self.post.title} ({self.pk})"
