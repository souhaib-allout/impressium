"""print URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from clientside import views

urlpatterns = [

    # path('tinymce/', include('tinymce.urls')),

    path('admin/', admin.site.urls),

    path('', views.index),
    path('product/<int:id>', views.product),
    path('products/<str:category>', views.productsbyCategory),

    path('products', views.products),

    path('search', views.search),
    path('onsearch', views.onsearch, name='onsearch'),

    path('download', views.download),

    path('addtppan', views.addtppan),
    path('deleteppan', views.deleteppan),
    path('updatepanpage/<int:id>', views.updatepanpage),
    path('updatepan', views.updatepan),
    path('duplicatepan', views.duplicatepan),

    path('cart', views.cart),
    path('deleveryfilter', views.deleveryfilter),
    path('filecontrolefilter', views.filecontrolefilter),

    path('contact', views.contact),
    path('sendmessage', views.sendmessage),

    path('login', views.login),
    path('logincheck', views.logincheck),

    path('logup', views.logup),
    path('logupcheck', views.logupcheck),

    path('logoutcheck', views.logoutcheck),

    path('dashboard', views.dashboard),

    path('profile', views.profile),
    path('updateprofile', views.updateprofile),

    path('adresses', views.adresses),
    path('updateadresse', views.updateadresse),
]
