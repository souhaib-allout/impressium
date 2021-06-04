import os
from wsgiref.util import FileWrapper

from django.contrib.auth import authenticate, login as loginnow, logout
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from clientside.models import *
from django.http import HttpResponse, JsonResponse, FileResponse
from django.contrib.auth.models import User
from django.db.models import Q, Count
import static
from django.core import serializers


# Create your views here.

def index(request):
    newarticles = Article.objects.order_by('-id')[:5]
    # topsearch = CategoryHistory.objects.annotate(nb_search=Count('title')).order_by('nb_search')[0:8]
    return render(request, 'index.html',
                  {'newarticles': newarticles, })


def login(request):
    categories = Category.objects.all()
    return render(request, 'login.html', {'categories': categories})


def logincheck(request):
    if (request.method == 'POST'):
        username = User.objects.get(email=request.POST['email'])

        user = authenticate(request, username=username.username, password=request.POST['password'])
        if user is not None:
            loginnow(request, user)
            if request.user.is_authenticated:
                return redirect('/dashboard')

            if not request.user.is_authenticated:
                return HttpResponse('not loged')

            return HttpResponse('good')
        else:
            return HttpResponse('bad')


def logup(request):
    categories = Category.objects.all()
    return render(request, 'logup.html', {'categories': categories})


def logupcheck(request):
    if (request.method == 'POST'):
        if (request.POST['password1'] == request.POST['password2']):
            user = User.objects.create_user(username=request.POST['name'] + ' ' + request.POST['lastname'],
                                            first_name=request.POST['name'],
                                            last_name=request.POST['lastname'], email=request.POST['mail'],
                                            password=request.POST['password1'])
            Client.objects.create(user_id=user.id, type=request.POST['type'], civilite=request.POST['civilite'],
                                  tele=request.POST['tele'])
            return redirect('/dashboard')
        else:
            return redirect('/')


def logoutcheck(request):
    logout(request)
    # return HttpResponse('good')
    return redirect('/login')


def dashboard(request):
    categories = Category.objects.all()
    return render(request, 'profile/dashboard.html', {'categories': categories})


def profile(request):
    categories = Category.objects.all()
    return render(request, 'profile/profile.html', {'categories': categories})


def updateprofile(request):
    if (request.method == "POST"):
        request.user.username = request.POST['name'] + ' ' + request.POST['lastname']
        request.user.first_name = request.POST['name']
        request.user.last_name = request.POST['lastname']
        request.user.email = request.POST['mail']
        Client.objects.update_or_create(user_id=request.user.id,
                                        defaults={
                                            'type': request.POST['type'],
                                            'civilite': request.POST['civilite'],
                                            'tele': request.POST['tele'],
                                        })
        request.user.save()
        if 'changepasswpord' in request.POST:
            if request.POST['newpassword'] == request.POST['newpassword2']:
                if check_password(request.POST['password1'], request.user.password):
                    request.user.password = make_password(request.POST['newpassword'], salt=None, hasher='default')
                else:
                    return HttpResponse('password inccorect')
            else:
                return HttpResponse('passwprod dosent match')
    return redirect('/profile')


def adresses(request):
    return render(request, 'profile/adresses.html')


def updateadresse(request):
    if (request.method == 'POST'):
        Client.objects.update_or_create(user_id=request.user.id,
                                        defaults={
                                            'adresse1': request.POST['adresse1'],
                                            'adresse2': request.POST['adresse2'],
                                            'codepostal': request.POST['codepostal'],
                                            'city': request.POST['ville'],
                                            'country': request.POST['pays']
                                        })
        return redirect('/adresses')
    else:
        return redirect('/')

    return redirect('/')


def contact(request):
    categories = Category.objects.all()
    return render(request, 'contact.html', {'categories': categories})


def sendmessage(request):
    if request.method == 'POST':
        Message.objects.create(full_name=request.POST['fullname'], email=request.POST['email'],
                               tele=request.POST['tele'], message=request.POST['message'])
        return redirect('/contact?messagesent=message sent')


def products(request):
    categories = Category.objects.all()
    products = Article.objects.order_by('-id').all()
    # return HttpResponse(products[4].articleimages[0].name)

    # return JsonResponse(products[0]['ArticleImage'])

    return render(request, 'products.html',
                  {'products': products, 'swiper-bundle.Css': 'good', 'categories': categories})


def product(request, id):
    product = Article.objects.get(id=id)
    # return HttpResponse(Article.objects.first().SpecificationArticle.FinitionSpecification.all)
    categories = Category.objects.all()
    realtedproducts = Article.objects.filter(childcategory=product.childcategory)[0:6]
    dilevies = Delivery.objects.all()
    return render(request, 'product.html',
                  {'product': product, 'categories': categories, 'realtedproducts': realtedproducts,
                   'dilevies': dilevies})


def productsbyCategory(request, category):
    categories = Category.objects.all()
    products = Article.objects.filter(childcategory__name=category).all()
    categoryid = ChildCategory.objects.get(name=category).id
    CategoryHistory.objects.create(childcategory_id=categoryid)
    category = ChildCategory.objects.get(name=category)
    return render(request, 'products.html',
                  {'products': products, 'swiper-bundle.Css': 'good', 'categories': categories, 'category': category})


def search(request):
    products = Article.objects.filter(
        Q(childcategory__name__contains=request.GET['rechercheinput']) | Q(
            title__contains=request.GET['rechercheinput']) | Q(
            info__contains=request.GET['rechercheinput']))
    if request.user.is_authenticated:
        Search.objects.create(user=request.user, title=request.GET['rechercheinput'])
    else:
        Search.objects.create(title=request.GET['rechercheinput'])
    categories = Category.objects.all()
    return render(request, 'searcharticle.html', {'products': products, 'searchtitle': request.GET['rechercheinput'],
                                                  'categories': categories})


def onsearch(request):
    if request.method == 'POST':
        lists = Article.objects.filter(title__contains=request.POST['searchtext']).values('title',
                                                                                          'articleimages__name',
                                                                                          'Sizearticle__price')[0:6]
        return JsonResponse(list(lists), safe=False)
    else:
        return HttpResponse('baaad')


# def searchbycols(request):

def download(request):
    # image= ArticleImage.objects.first().name
    # content =FileWrapper('ballon_2.jpg')
    # response = HttpResponse(content, content_type='application/pdf')
    # response['Content-Length'] = os.path.getsize('ballon_2.jpg')
    # response['Content-Disposition'] = 'attachment; filename=%s' % 'whatever_name_will_appear_in_download.pdf'
    # return response

    return FileResponse(open('static/files/file1.pdf', 'rb'))

def addtppan(request):
    if(request.method=='POST'):
        formatype,format,
        Pane.objects.create(article=request.articleid,)
    else:
        return redirect('/')
