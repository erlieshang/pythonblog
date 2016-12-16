from django.forms import modelform_factory
from .models import Post, Comment
from django import forms
from haystack.forms import SearchForm


PostForm = modelform_factory(Post, fields=("title", "text"))

CommentForm = modelform_factory(Comment, fields=("content",))


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', min_length=8, max_length=100, widget=forms.PasswordInput)
    email = forms.EmailField(label='Email')
    date_of_birth = forms.DateField(label='DateOfBirth')
    avatar = forms.ImageField(label='Avatar', required=False)


class DateRangeSearchForm(SearchForm):
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    def search(self):
        sqs = super(DateRangeSearchForm, self).search()
        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['start_date']:
            sqs = sqs.filter(pub_date__gte=self.cleaned_data['start_date'])

        if self.cleaned_data['end_date']:
            sqs = sqs.filter(pub_date__lte=self.cleaned_data['end_date'])

        return sqs
