from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'text', 'post_id')
        widgets = {
            'post_id': forms.HiddenInput(),
        }
