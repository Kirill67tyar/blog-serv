from django import forms

from blog.models import Comment


class EmailForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        # или
        # exclude = ('post', 'author', 'created', 'updated', 'active',)
