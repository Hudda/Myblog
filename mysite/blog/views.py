from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, Comment, Post
from .forms import CommentForm, PostForm


class CategoryView(generic.ListView):
    model = Category
    template_name = 'blog/category.html'
    context_object_name = 'category_post'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now(),
            category_name=self.kwargs['category_name']
            ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class IndexView(generic.ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'latest_post_list'
    paginate_by = 6
    queryset = Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['popular_post_list'] = Post.objects.filter(pub_date__lte=timezone.now()).order_by('-vote')[:3]
        context['categories'] = Category.objects.all()
        return context


class DetailView(generic.DetailView):
    model = Post
    template_name = 'blog/blog-single.html'

    def get_queryset(self):
        return Post.objects.filter(created_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm
        context['categories'] = Category.objects.all()
        return context

class DraftView(LoginRequiredMixin, generic.ListView):
    template_name = 'blog/draft.html'
    context_object_name = 'latest_draft_list'

    def get_queryset(self):
        return Post.objects.filter(
            pub_date__isnull=True
        ).order_by('-created_date')


def vote(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.session.get('has_voted', False):
        post.vote = F('vote') - 1
        post.save()
        request.session['has_voted'] = False
    else:
        post.vote = F('vote') + 1
        post.save()
        request.session['has_voted'] = True
    return HttpResponseRedirect(reverse('blog:detail', args=(post_id,)))

def get_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            post.comment_counter = F('comment_counter') + 1
            post.save()
            comment.save()
            return HttpResponseRedirect(reverse('blog:detail', args=(post_id,)))
    else:
        form = CommentForm()
    context = {'form': form,
            'post': post,}

    return render(request, 'blog/blog-single.html', context)

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:draft')
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})

@login_required
def publish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:index')

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:index')

def about(request):
    category = Category.objects.all()
    return render(request, 'blog/about.html', {'categories': category})
