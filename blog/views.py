from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse


def post_list(request):
	# Only show posts that are marked visible in portal settings (default True)
	posts = Post.objects.filter(portal__visible=True)
	paginator = Paginator(posts, 6)
	page_number = request.GET.get('page')
	posts_page = paginator.get_page(page_number)
	return render(request, 'blog/post_list.html', {'posts_page': posts_page})


def post_detail(request, slug):
	post = get_object_or_404(Post, slug=slug)
	return render(request, 'blog/post_detail.html', {'post': post})


def home(request):
	# Simple portfolio front page; you can extend later with projects and about info
	latest = Post.objects.filter(portal__visible=True).order_by('-published')[:3]
	return render(request, 'blog/home.html', {'latest': latest})


def contact(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		email = request.POST.get('email')
		subject = request.POST.get('subject') or 'Website contact'
		message = request.POST.get('message')

		full_message = f"From: {name} <{email}>\n\n{message}"
		send_mail(subject, full_message, settings.DEFAULT_FROM_EMAIL, [settings.EMAIL_HOST_USER], fail_silently=False)
		return HttpResponseRedirect(reverse('home') + '?sent=1')
	return HttpResponseRedirect(reverse('home'))
