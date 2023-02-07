from django import forms
from network.models import Post
class PostForm(forms.ModelForm):
    model=Post

    def __init__(self, *args, **kwargs):
        
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.request.user
        instance.save()

    class Meta: 
        model = Post
        fields = ['title', 'description']

    
        
