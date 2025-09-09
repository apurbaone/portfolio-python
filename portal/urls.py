from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('', views.dashboard, name='dashboard'),
    path('toggle/<int:pk>/', views.toggle_visibility, name='toggle_visibility'),
    path('new/', views.new_post, name='new_post'),
    path('edit', views.edit_index, name='edit_list_no_slash'),
    path('edit/', views.edit_index, name='edit_list'),
    path('edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('delete-image/<int:pk>/', views.delete_gallery_image, name='delete_gallery_image'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('preview/<int:pk>/', views.preview_post, name='preview_post'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('auth/', views.auth_index, name='auth_index'),
    path('auth/toggle-staff/<int:pk>/', views.toggle_staff, name='toggle_staff'),
]
