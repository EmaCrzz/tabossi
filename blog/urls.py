from django.urls import path
from . import views

urlpatterns = [
    path('', views.section_list, name='section_list'),
    path('sections/post/<int:pk>/', views.posts_sections, name='posts_sections'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/add/comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('post/list/comment/<int:pk>/', views.list_comment, name='list_comment'),
    path('gobierno/', views.avatar_list, name='avatar_list'),
    path('ordenanzas/', views.ordenanzas_list, name='ordenanzas_list')
]
