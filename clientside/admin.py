import self
from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.contrib.admin import AdminSite, site
from django.contrib.auth.models import Group
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.urls import path

# from tinymce.widgets import TinyMCE
from clientside.models import *

# Register your models here.
# AdminSite.site_url(test)
admin.site.unregister(User)
admin.site.site_header = 'Admin panel'
AdminSite.index_template = 'chart.html'


#########Client
class ClientLine(admin.StackedInline):
    model = Client


class ModelAdminClient(admin.ModelAdmin):
    inlines = [ClientLine]
    # list_display = ['user']
    exclude = ['created_at']


admin.site.register(User, ModelAdminClient)
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


admin.site.register(FontColor, AdminfontColorModal)


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
    options = forms.CharField(widget=CKEditorWidget(), label='Options - Finitions')
    conseil = forms.CharField(widget=CKEditorWidget(), label='Conseils Techniques')
    complementes = forms.CharField(widget=CKEditorWidget(), label='Produits complémentaires')


class AdminArticle(admin.ModelAdmin):
    form = ArticleForm
    fields = ['title', 'childcategory', 'info', 'options', 'conseil', 'complementes', 'pdf']
    exclude = ['created_at']
    list_display = ['title', 'childcategory']
    list_filter = ['created_at', 'childcategory']
    inlines = [ArticleImagesLine, SpecificationLine]
    list_per_page = 15
    search_fields = ['title', 'childcategory']


admin.site.register(Article, AdminArticle)


################# Category
class AdminCategory(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']
    exclude = ['created_at']


admin.site.register(Category, AdminCategory)


################# ChildCategory
class AdminChildCategory(admin.ModelAdmin):
    list_display = ['name', 'Category', 'created_at']
    search_fields = ['name', 'Category']
    list_filter = ['Category', 'created_at']
    exclude = ['created_at']


admin.site.register(ChildCategory, AdminChildCategory)


###############Best article
class ModalAdminBestArticle(admin.ModelAdmin):
    exclude = ['created_at']


admin.site.register(Bestarticle, ModalAdminBestArticle)


############Messages
# class MessageLine(admin.TabularInline):
#     admin.site.disable_action('delete_selected')
class ModalAdminMessage(admin.ModelAdmin):
    list_filter = ['email', 'created_at']
    search_fields = ['email', 'full_name', 'tele', 'message']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Message, ModalAdminMessage)


##############Search
# admin.site.register(Search)


#################Delevery
class ModalAdminDelevery(admin.ModelAdmin):
    list_display = ['name', 'price']
    list_filter = ['name', 'price']
    search_fields = ['name', 'price']
    exclude = ['created_at']


admin.site.register(Delivery, ModalAdminDelevery)


###################Pane
class ModalAdminPane(admin.ModelAdmin):
    list_display = ['article', 'user']
    list_filter = ['article', 'user']
    search_fields = ['article', 'user']

    # exclude = ['created_at']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Pane, ModalAdminPane)
admin.site.register(FileControle)


class PanehistoryLine(admin.StackedInline):
    model = LastPane
    readonly_fields = ['FileControle', 'CostumQuantity', 'ArticleDesign', 'size', 'formattype', 'paperType',
                       'paperColor', 'fontColor','side','orientation','finition','Quantity','CostumQuantity']
    exclude = ['created_at', 'Delevery']
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj):
        return False


# admin.site.register(LastPane)

class ModalAdminCommande(admin.ModelAdmin):
    inlines = [PanehistoryLine]
    readonly_fields = ['User', 'total', 'delevery', 'created_at']
    list_display = ['User', 'total', 'created_at']
    list_filter = ['created_at']
    search_fields = ['User', 'total', 'created_at']
    list_per_page = 15

    def has_add_permission(self, request, obj=None):
        return False

    # exclude = ['created_at']


admin.site.register(Commande, ModalAdminCommande)
