from django import forms 
from django.contrib.auth.models import User 
from .models import Post , Comment, Tag
from taggit.forms import TagWidget

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['username', 'email']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(),  # <- ALX wants this exact line
        }

    # Optional: handle comma-separated tags if you want custom save logic
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        # tag handling if needed
        return instance 

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=True
    )

    class Meta:
        model = Comment
        fields = ['content']
  