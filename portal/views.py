from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse
from blog.models import Post
from .models import PortalPost, Visitor
from django.http import JsonResponse
from django.contrib import messages
from .forms import PostForm, GalleryImageForm
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from blog.models import PostImage
from django.shortcuts import reverse
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.auth.models import User, Group
import pathlib


class LoginView(auth_views.LoginView):
    template_name = 'portal/login.html'


@login_required
def dashboard(request):
    posts = Post.objects.all().order_by('-published')
    # ensure PortalPost exists for each
    for p in posts:
        PortalPost.objects.get_or_create(post=p)
    portal_posts = PortalPost.objects.select_related('post').all().order_by('-post__published')
    recent_visitors = Visitor.objects.order_by('-timestamp')[:20]
    all_visitors = Visitor.objects.order_by('-timestamp')[:200]
    return render(request, 'portal/dashboard.html', {
        'portal_posts': portal_posts,
        'recent_visitors': recent_visitors,
        'all_visitors': all_visitors,
        'post_count': posts.count(),
    })


@login_required
def toggle_visibility(request, pk):
    if request.method != 'POST':
        return JsonResponse({'ok': False}, status=405)
    pp = get_object_or_404(PortalPost, pk=pk)
    pp.visible = not pp.visible
    pp.save()
    return JsonResponse({'ok': True, 'visible': pp.visible})


@login_required
def new_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    gallery_form = GalleryImageForm()
    if request.method == 'POST' and form.is_valid():
        post = form.save()
        # handle gallery files (if sent as multiple 'gallery' file inputs)
        for f in request.FILES.getlist('gallery'):
            PostImage.objects.create(post=post, image=f)
        messages.success(request, 'New post created')
        return redirect('portal:dashboard')
    # if POST but not valid, surface an error message so user sees why
    if request.method == 'POST' and not form.is_valid():
        messages.error(request, 'Please fix the errors below and try again')
    return render(request, 'portal/post_form.html', {'form': form, 'gallery_form': gallery_form, 'is_new': True})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    gallery_form = GalleryImageForm()
    if request.method == 'POST' and form.is_valid():
        post = form.save()
        for f in request.FILES.getlist('gallery'):
            PostImage.objects.create(post=post, image=f)
        messages.success(request, 'Post updated')
        return redirect('portal:dashboard')
    if request.method == 'POST' and not form.is_valid():
        messages.error(request, 'Please fix the errors below and try again')
    return render(request, 'portal/post_form.html', {'form': form, 'gallery_form': gallery_form, 'post': post, 'is_new': False})


@require_POST
@login_required
def delete_gallery_image(request, pk):
    img = get_object_or_404(PostImage, pk=pk)
    post_pk = img.post.pk
    img.delete()
    return redirect(reverse('portal:edit_post', args=[post_pk]))

@require_http_methods(['POST'])
@login_required
def delete_post(request, pk):
    # delete both Post and linked PortalPost
    p = get_object_or_404(Post, pk=pk)
    # redirect target
    redirect_to = reverse('portal:edit_list')
    p.delete()
    messages.success(request, 'Post deleted')
    return redirect(redirect_to)


@login_required
def preview_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # reuse public post_detail template if available
    return render(request, 'blog/post_detail.html', {'post': post, 'preview': True})


@login_required
def edit_index(request):
    """List posts with edit links (handles /portal/edit/)."""
    posts = Post.objects.all().order_by('-published')
    return render(request, 'portal/edit_list.html', {'posts': posts})


@require_POST
@login_required
def upload_image(request):
    """Receive an uploaded image and save to MEDIA; return JSON with URL.

    This endpoint is used by the portal editor to upload an image and insert it into
    the post body as an <img> tag.
    """
    # support both TinyMCE (file) and our inline control (image)
    f = request.FILES.get('file') or request.FILES.get('image')
    if not f:
        return JsonResponse({'error': 'no file'}, status=400)
    # ensure safe filename
    name = pathlib.Path(f.name).name
    save_path = f'blog/uploads/{name}'
    filename = default_storage.save(save_path, f)
    url = settings.MEDIA_URL + filename
    # TinyMCE expects JSON with `location` key, other clients may expect `url`.
    return JsonResponse({'location': url, 'url': url})


@login_required
def auth_index(request):
    """Simple users & groups listing for portal-level auth management (read+toggle staff)."""
    users = User.objects.all().order_by('-is_superuser', '-is_staff', 'username')
    groups = Group.objects.all().order_by('name')
    return render(request, 'portal/auth.html', {'users': users, 'groups': groups})


@require_POST
@login_required
def toggle_staff(request, pk):
    u = get_object_or_404(User, pk=pk)
    # Prevent demoting the last superuser via portal
    if u == request.user and u.is_superuser:
        # don't change superuser status for self
        return redirect('portal:auth_index')
    u.is_staff = not u.is_staff
    u.save()
    return redirect('portal:auth_index')
