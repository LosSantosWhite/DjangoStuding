from django.urls import path
from . import views

app_name = 'app_news'

urlpatterns = [
    path('<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
]
