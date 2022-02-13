from django import forms
from django.forms.widgets import HiddenInput
from .models import Comment, Post
#
#
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','body']

    def __init__(self, *args, **kwargs):
        hidden = kwargs.pop('hidden', None)
        super(CommentForm, self).__init__(*args, **kwargs)
        if hidden:
            self.fields['name'].widget = HiddenInput()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'bode', 'author', 'status']
