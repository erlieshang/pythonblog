from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class BlogUser(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='blog/upload/avatar', blank=True)
    date_of_birth = models.DateField(verbose_name='Date of Birth', blank=True)


class Post(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    pub_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.pub_date = timezone.now()
        self.save()

    def save_draft(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})


class ImageInPost(models.Model):
    image = models.ImageField(upload_to='blog/upload/image')


class Comment(models.Model):
    author = models.ForeignKey(User)
    bound_to_post = models.ForeignKey(Post)
    floor = models.IntegerField(default=1)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.content
