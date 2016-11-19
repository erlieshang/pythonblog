from .models import Post
from haystack import indexes
class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()