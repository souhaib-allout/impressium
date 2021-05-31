from clientside.models import *


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title']
        title = forms.DateField()
