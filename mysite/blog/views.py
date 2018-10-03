from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone

from .models import Comment, Post
from .forms import CommentForm

class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        return Post.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now())


def vote(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.vote = F('vote') + 1
    post.save()
    return HttpResponseRedirect(reverse('blog:detail', args=(post_id,)))

def get_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('blog:detail', args=(post_id,)))
    else:
        form = CommentForm()

    return render(request, 'blog/comment.html', {'form': form})