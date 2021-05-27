from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms import ModelForm
from suit_ckeditor.widgets import CKEditorWidget

from clientside import models

# Register your models here.
# from clientside.models import *
#############Group
admin.site.unregister(Group)


# ##########Article image
class ArticleImagesLine(admin.TabularInline):
    model = models.ArticleImage
    extra = 1


# class ArticleCategoryLine(admin.TabularInline):
#     model = models.Category
#
# class ArticleChildCategoryLine(admin.TabularInline):
#     model = models.ChildCategory

################# Article
class PageForm(ModelForm):
    class Meta:
        widgets = {
            'info': CKEditorWidget(editor_options={'startupFocus': True}),
            'options': CKEditorWidget(editor_options={'startupFocus': True}),
            'conseil': CKEditorWidget(editor_options={'startupFocus': True}),
            'complementes': CKEditorWidget(editor_options={'startupFocus': True}),
        }


class AdminArticle(admin.ModelAdmin):
    form = PageForm
    fields = ['title', 'childcategory', 'info', 'options', 'conseil', 'complementes']
    list_display = ['title', 'childcategory']
    list_filter = ['title','created_at','childcategory']
    inlines = [ArticleImagesLine]
    list_per_page = 15
    search_fields = ['title','childcategory']
    view_on_site = False






admin.site.register(models.Article, AdminArticle)


################# Category
class AdminCategory(admin.ModelAdmin):
    fields = ['name']


admin.site.register(models.Category)


################# ChildCategory
class AdminChildCategory(admin.ModelAdmin):
    fields = ['Category', 'name']


admin.site.register(models.ChildCategory)

###############Best article
admin.site.register(models.Bestarticle)

############Messages
admin.site.register(models.Message)