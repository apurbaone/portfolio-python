from django import forms
from blog.models import Post, PostImage


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'excerpt', 'banner_image', 'body']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'portal-input portal-title',
                'placeholder': 'Enter a compelling title'
            }),
            'slug': forms.TextInput(attrs={'class': 'portal-input'}),
            'excerpt': forms.Textarea(attrs={'class': 'portal-input', 'rows': 2}),
            'body': forms.Textarea(attrs={'class': 'portal-input portal-body', 'rows': 12}),
        }


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['image', 'caption']