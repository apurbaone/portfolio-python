from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'published')
	prepopulated_fields = {'slug': ('title',)}
	fields = ('title', 'slug', 'excerpt', 'image', 'body')
	search_fields = ('title', 'excerpt', 'body')
