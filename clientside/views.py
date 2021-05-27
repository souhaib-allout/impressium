from django.contrib.auth import authenticate, login as loginnow, logout
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from clientside.models import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.core import serializers


# Create your views here.

def index(request):
    newarticles = Article.objects.order_by('-id')[:5]
    # bestarticles = Bestarticle.objects.all()
    bestarticles = Article.objects.filter(bestarticle__id__isnull=False)
    # return HttpResponse(bestarticles)
    topsearch = Search.objects.annotate(nb_search=Count('title')).order_by('nb_search')[0:8]

    # for articl in bestarticles:
    #     print(articl.bestarticle.first().id)
    # print('article :' + str(articleb.id))
    # for size in articleb.article.Sizearticle.all():
    #     print('price: ' + str(size.price))

    # return HttpResponse('good')
    return render(request, 'index.html',
                  {'newarticles': newarticles, 'bestarticles': bestarticles, 'topsearch': topsearch})


def product(request, id):
    product = Article.objects.filter(id=id).first()
    return render(request, 'product.html', {'product': product})


def login(request):
    return render(request, 'login.html')


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
    return render(request, 'logup.html')


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
    return render(request, 'profile/dashboard.html')


def profile(request):
    return render(request, 'profile/profile.html')


def updateprofile(request):
    if (request.method == "POST"):
        request.user.username = request.POST['name'] + ' ' + request.POST['lastname']
        request.user.first_name = request.POST['name']
        request.user.last_name = request.POST['lastname']
        request.user.email = request.POST['mail']
        request.user.ClientUser.type = request.POST['type']
        request.user.ClientUser.civilite = request.POST['civilite']
        request.user.ClientUser.tele = request.POST['tele']
        request.user.save()
        request.user.ClientUser.save()
        if 'changepasswpord' in request.POST:
            if request.POST['newpassword'] == request.POST['newpassword2']:
                if check_password(request.POST['password1'], request.user.password):
                    request.user.password = make_password(request.POST['newpassword'], salt=None, hasher='default')
                else:
                    return HttpResponse('password inccorect')
            else:
                return HttpResponse('passwprod dosent match')

    return redirect('/profile')


def contact(request):
    return render(request, 'contact.html')


def sendmessage(request):
    if request.method == 'POST':
        Message.objects.create(full_name=request.POST['fullname'], email=request.POST['email'],
                               tele=request.POST['tele'], message=request.POST['message'])
        return redirect('/contact?messagesent=message sent')


def products(request):
    products = Article.objects.order_by('-id').all()
    # return HttpResponse(products[4].articleimages[0].name)

    # return JsonResponse(products[0]['ArticleImage'])

    return render(request, 'products.html', {'products': products, 'swiper-bundle.Css': 'good'})


def search(request):
    products = Article.objects.filter(
        Q(type__contains=request.GET['rechercheinput']) | Q(title__contains=request.GET['rechercheinput']) | Q(
            info__contains=request.GET['rechercheinput']))
    if request.user.is_authenticated:
        Search.objects.create(user=request.user, title=request.GET['rechercheinput'])
    else:
        Search.objects.create(title=request.GET['rechercheinput'])
    return render(request, 'searcharticle.html', {'products': products, 'searchtitle': request.GET['rechercheinput']})


def onsearch(request):
    if request.method == 'POST':
        lists = Article.objects.filter(title__contains=request.POST['searchtext']).values('title', 'articleimages__name','Sizearticle__price')[0:6]
        return JsonResponse(list(lists),safe=False)
    else:
        return HttpResponse('baaad')

# def searchbycols(request):
