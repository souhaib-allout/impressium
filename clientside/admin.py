from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.contrib.auth.models import Group

# from tinymce.widgets import TinyMCE

from clientside.models import *

# Register your models here.


#############Group
admin.site.unregister(Group)


# ##########Article image
class ArticleImagesLine(admin.TabularInline):
    model = ArticleImage
    exclude = ['created_at']
    extra = 1


################# Article


# class ArticleForm(forms.ModelForm):
#     info = forms.CharField(widget=TinyMCE(attrs={'cols': 20, 'rows': 20}))
#     title=forms.TextInput()

class ArticleForm(forms.ModelForm):
    info = forms.CharField(widget=CKEditorWidget())
    options = forms.CharField(widget=CKEditorWidget())
    conseil = forms.CharField(widget=CKEditorWidget())
    complementes = forms.CharField(widget=CKEditorWidget())


class AdminArticle(admin.ModelAdmin):
    form = ArticleForm
    fields = ['title', 'childcategory', 'info', 'options', 'conseil', 'complementes']
    exclude = ['created_at']
    list_display = ['title', 'childcategory']
    list_filter = ['title', 'created_at', 'childcategory']
    inlines = [ArticleImagesLine]
    list_per_page = 15
    search_fields = ['title', 'childcategory']


admin.site.register(Article, AdminArticle)


################# Category
class AdminCategory(admin.ModelAdmin):
    fields = ['name']


admin.site.register(Category)


################# ChildCategory
class AdminChildCategory(admin.ModelAdmin):
    fields = ['Category', 'name']


admin.site.register(ChildCategory)

###############Best article
admin.site.register(Bestarticle)

############Messages
admin.site.register(Message)
