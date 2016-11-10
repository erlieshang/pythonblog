from django.views import generic
from .models import Post
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import PostForm


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        return Post.objects.filter(pub_date__isnull=False).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'


def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.publish()
            return redirect('blog:detail', pk=post.pk)
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})