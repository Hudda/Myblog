from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:post_id>/vote/', views.vote, name='vote'),
    path('<int:post_id>/comment/', views.get_comment, name='comment'),
    path('new/', views.add_post, name='add_post'),
    path('<int:pk>/edit/', views.edit_post, name='post_edit'),
    path('drafts/', views.DraftView.as_view(), name='draft'),
    path('<int:pk>/publish/', views.publish_post, name='publish_post'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete')
]