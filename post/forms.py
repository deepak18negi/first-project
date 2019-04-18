from django import forms
from django.contrib.auth.models import User
from post.models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(label='', required=False, widget=forms.Textarea(
        attrs={'class': 'form-control textfield', 'rows': 5, 'cols': 70}))
    image = forms.FileField(label='')

    class Meta:
        model = Post
        fields = {'content',
                  'image'}
