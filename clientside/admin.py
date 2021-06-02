from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.contrib.auth.models import Group

# from tinymce.widgets import TinyMCE

from clientside.models import *

# Register your models here.


#############Group
admin.site.unregister(Group)


#######PaperSize
class ModelAdminSize(admin.ModelAdmin):
    exclude = ['created_at']


admin.site.register(Size1, ModelAdminSize)


#######PaperType
class ModelAdminPaperType(admin.ModelAdmin):
    exclude = ['created_at']


admin.site.register(PaperType, ModelAdminPaperType)


#######PaperColor
class ModelAdminPaperColor(admin.ModelAdmin):
    exclude = ['created_at']


admin.site.register(PaperColor, ModelAdminPaperColor)


#######Side
class ModelAdminSide(admin.ModelAdmin):
    exclude = ['created_at']


admin.site.register(Side, ModelAdminSide)


#######Orientation
class ModelAdminOrientation(admin.ModelAdmin):
    exclude = ['created_at']


admin.site.register(Orientation, ModelAdminOrientation)


#######Finition
class ModelAdminFinition(admin.ModelAdmin):
    exclude = ['created_at']


admin.site.register(Finition, ModelAdminFinition)

#############Specification
class SpecificationLine(admin.StackedInline):
    model = Specification
    exclude = ['created_at']
    extra = 1


###########Article image
class ArticleImagesLine(admin.TabularInline):
    model = ArticleImage
    exclude = ['created_at']
    extra = 1


################ Article

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
    list_filter = ['created_at', 'childcategory']
    inlines = [ArticleImagesLine, SpecificationLine]
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
# class MessageLine(admin.TabularInline):
#     admin.site.disable_action('delete_selected')
class ModalAdminMessage(admin.ModelAdmin):
    actions = None
    list_filter = ['email','created_at']
    search_fields = ['email','full_name','tele','message']



admin.site.register(Message,ModalAdminMessage)
