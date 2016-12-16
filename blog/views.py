from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post, ImageInPost, Comment, BlogUser
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm, RegisterForm
from django.conf import settings
from haystack.forms import SearchForm


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

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        context['comment_form'] = form
        return context


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if request.POST.get('operation') == 'publish':
                post.publish()
            else:
                post.save_draft()
            return redirect('blog:detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('blog:index')
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            original_user = User.objects.create_user(username, email, password)
            original_user.save()
            date_of_birth = form.cleaned_data['date_of_birth']
            instance = BlogUser()
            if 'avatar' in request.FILES:
                instance.avatar = request.FILES['avatar']
                if not validate_filename(instance.avatar.name):
                    instance = BlogUser()
            else:
                instance = BlogUser()
            instance.date_of_birth = date_of_birth
            instance.user = original_user
            instance.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})


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
        if request.POST.get('operation') == 'Confirm':
            post.delete()
            return redirect('blog:list')
        else:
            return redirect('blog:detail', pk=post.pk)
    return render(request, 'blog/remove.html', {'post': post})


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.floor = Comment.objects.all().count() + 1
            comment.bound_to_post = post
            comment.save()
    return redirect('blog:detail', pk=post.pk)


def img_upload(request):
    if request.method == 'POST':
        instance = ImageInPost(image=request.FILES['ImgName'])
        if validate_filename(instance.image.name):
            instance.save()
            return HttpResponse(instance.image.url, content_type="text/html", charset="utf-8")
        else:
            return HttpResponse("error| invalid extension", content_type="text/html", charset="utf-8")
    else:
        return HttpResponse("error| upload failed", content_type="text/html", charset="utf-8")


def validate_filename(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

