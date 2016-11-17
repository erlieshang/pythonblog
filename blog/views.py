from django.views import generic
from .models import Post
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import PostForm


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        return Post.objects.filter(pub_date__isnull=False).order_by('-pub_date')[:5]


class ListView(generic.ListView):
    template_name = 'blog/list.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(pub_date__isnull=False).order_by('-pub_date')


class DraftView(generic.ListView):
    template_name = 'blog/drafts.html'
    context_object_name = 'draft_list'

    def get_queryset(self):
        return Post.objects.filter(pub_date__isnull=True).order_by('-created_date')


class DetailView(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if request.POST.get('submit') == 'publish':
                post.publish()
            else:
                post.save_draft()
            return redirect('blog:detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish()
            return redirect('blog:detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})


@login_required
def post_pub(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:detail', pk=post.pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        if request.POST.get('submit') == 'Confirm':
            post.delete()
            return redirect('blog:list')
        else:
            return redirect('blog:detail', pk=post.pk)
    return render(request, 'blog/remove.html', {'post': post})
