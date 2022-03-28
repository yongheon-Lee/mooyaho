from django import forms
from .post_models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'hiking_img',
            'title',
            'mountain_name',
            'content',
            'rating'
        ]
