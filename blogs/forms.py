from django import forms
from .models import Post

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','slug', 'content']
