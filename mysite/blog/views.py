from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone

from .models import Comment, Post
from .forms import CommentForm, PostForm

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
        return Post.objects.filter(created_date__lte=timezone.now())


class DraftView(generic.ListView):
    template_name = 'blog/post_drafts.html'
    context_object_name = 'latest_draft_list'

    def get_queryset(self):
        return Post.objects.filter(
            pub_date__isnull=True
        ).order_by('-created_date')


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

    return render(request, 'blog/detail.html', {'form': form, 'post':post})

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:draft')
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = timezone.now()
            post.save()
            return redirect('blog:detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})
