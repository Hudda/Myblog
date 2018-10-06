from django import forms

from .models import Comment, Post

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'email', 'text',)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('topic_text', 'content_text', 'image',)