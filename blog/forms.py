from django.forms import modelform_factory
from .models import Post


PostForm = modelform_factory(Post, fields=("title", "text"))