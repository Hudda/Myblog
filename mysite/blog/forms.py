from django import forms

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Comment, Post

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'email', 'text',)


class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('category_name', 'picture', 'topic_text', 'content_text')
		widgets = {
			'content_text': SummernoteWidget(),
			}