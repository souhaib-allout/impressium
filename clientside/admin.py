from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.contrib.auth.models import Group

# from tinymce.widgets import TinyMCE

from clientside.models import *

# Register your models here.
admin.site.unregister(User)
#########Client
class ClientLine(admin.StackedInline):
    model = Client

class ModelAdminClient(admin.ModelAdmin):
    inlines = [ClientLine]
    # list_display = ['user']
    exclude = ['created_at']

admin.site.register(User,ModelAdminClient)
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
#############Font color
class AdminfontColorModal(admin.ModelAdmin):
    exclude = ['created_at']

admin.site.register(FontColor,AdminfontColorModal)
#######PaperColor
class ModelAdminPaperColor(admin.ModelAdmin):
    exclude = ['created_at']


admin.site.register(PaperColor, ModelAdminPaperColor)
#######Quantite
class ModelAdminPaperColor(admin.ModelAdmin):
    exclude = ['created_at']


admin.site.register(Quantity, ModelAdminPaperColor)

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

###########Article image
class Quantite(admin.TabularInline):
    model = ArticleImage
    exclude = ['created_at']
    extra = 1

################ Article

class ArticleForm(forms.ModelForm):
    info = forms.CharField(widget=CKEditorWidget(), label='Infos produit')
    options = forms.CharField(widget=CKEditorWidget(),label='Options - Finitions')
    conseil = forms.CharField(widget=CKEditorWidget(),label='Conseils Techniques')
    complementes = forms.CharField(widget=CKEditorWidget(),label='Produits complémentaires')


class AdminArticle(admin.ModelAdmin):
    form = ArticleForm
    fields = ['title', 'childcategory', 'info', 'options', 'conseil', 'complementes','pdf']
    exclude = ['created_at']
    list_display = ['title', 'childcategory']
    list_filter = ['created_at', 'childcategory']
    inlines = [ArticleImagesLine, SpecificationLine]
    list_per_page = 15
    search_fields = ['title', 'childcategory']




admin.site.register(Article, AdminArticle)


################# Category
class AdminCategory(admin.ModelAdmin):
    # fields = ['name']
    exclude = ['created_at']



admin.site.register(Category,AdminCategory)


################# ChildCategory
class AdminChildCategory(admin.ModelAdmin):
    # fields = ['Category', 'name']
    exclude = ['created_at']



admin.site.register(ChildCategory,AdminChildCategory)


###############Best article
class ModalAdminBestArticle(admin.ModelAdmin):
    exclude = ['created_at']


admin.site.register(Bestarticle,ModalAdminBestArticle)


############Messages
# class MessageLine(admin.TabularInline):
#     admin.site.disable_action('delete_selected')
class ModalAdminMessage(admin.ModelAdmin):
    actions = None
    list_filter = ['email', 'created_at']
    search_fields = ['email', 'full_name', 'tele', 'message']


admin.site.register(Message, ModalAdminMessage)

##############Search
admin.site.register(Search)
#################Delevery
class ModalAdminDelevery(admin.ModelAdmin):
    actions = None
    list_filter = ['name', 'price']
    search_fields = ['name', 'price']
    exclude = ['created_at']

admin.site.register(Delivery,ModalAdminDelevery)

###################Pane
admin.site.register(Pane)
admin.site.register(FileControle)