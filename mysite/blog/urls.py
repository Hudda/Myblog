from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:post_id>/vote/', views.vote, name='vote'),
    path('<int:post_id>/comment/', views.get_comment, name='comment'),
    path('post/', views.add_post, name='add_post'),
]