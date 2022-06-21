from django import forms
from .models import ArticleColumn, ArticlePost, Comments, ArticleTag


class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ('column',)

class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ('title', 'body')

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('commentator', 'body',)

class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ('tag',)