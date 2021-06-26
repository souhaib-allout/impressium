import datetime
import os
from wsgiref.util import FileWrapper

from django.contrib.auth import authenticate, login as loginnow, logout
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from clientside.models import *
from django.http import HttpResponse, JsonResponse, FileResponse
from django.contrib.auth.models import User
from django.db.models import Q, Count
import json
import static
from django.core import serializers
from django.core.files.storage import default_storage

try:
    from urllib.parse import urlencode
    from urllib.request import build_opener, Request, HTTPHandler
    from urllib.error import HTTPError, URLError
except ImportError:
    from urllib import urlencode
    from urllib2 import build_opener, Request, HTTPHandler, HTTPError, URLError
import json


# Create your views here.

def index(request):
    newarticles = Article.objects.order_by('-id')[:5]
    article=Article.objects.get(id=6)
    min=str(article.SpecificationArticle.minprice)
    print(min)
    # topsearch = CategoryHistory.objects.annotate(nb_search=Count('title')).order_by('nb_search')[0:8]
    # for newarticle in newarticles:
    #     if newarticle.SpecificationArticle :
    #         print(newarticle.SpecificationArticle)
    return render(request, 'index.html',
                  {'newarticles': newarticles, })


def login(request):
    categories = Category.objects.all()
    return render(request, 'profile/login.html', {'categories': categories})


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
    return render(request, 'profile/logup.html', {'categories': categories})


def logupcheck(request):
    if (request.method == 'POST'):
        if (request.POST['password1'] == request.POST['password2']):
            user = User.objects.create_user(username=request.POST['name'] + ' ' + request.POST['lastname'],
                                            first_name=request.POST['name'],
                                            last_name=request.POST['lastname'], email=request.POST['mail'],
                                            password=request.POST['password1'])
            Client.objects.create(user_id=user.id, type=request.POST['type'], civilite=request.POST['civilite'],
                                  tele=request.POST['tele'])
            body = render_to_string('mails/signupMail.html', {'user': user.username})
            msg = EmailMessage('test', body, 'info@impresiion.com', [user.email])
            msg.content_subtype = "html"
            msg.send()
            return redirect('/dashboard')
        else:
            return redirect('/')


def logoutcheck(request):
    logout(request)
    # return HttpResponse('good')
    return redirect('/login')


def dashboard(request):
    categories = Category.objects.all()
    nbcommandes = Commande.objects.filter(User=request.user).all()
    return render(request, 'profile/dashboard.html', {'categories': categories, 'nbcommandes': nbcommandes})


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


def mydesigns(request):
    designs = Pane.objects.filter(user=request.user, ArticleDesign__isnull=False).all()
    return render(request, 'profile/designs.html', {'designs': designs})


def downloadmydesign(request):
    if (request.method == 'POST'):
        designs = Pane.objects.get(id=request.POST['paneid'], user=request.user)
        return FileResponse(open(designs.ArticleDesign.name, 'rb'))
    else:
        return redirect('/mes_designs')


def contact(request):
    categories = Category.objects.all()
    return render(request, 'contact.html', {'categories': categories})


def sendmessage(request):
    if request.method == 'POST':
        Message.objects.create(full_name=request.POST['fullname'], subject=request.POST['subject'],
                               email=request.POST['email'],
                               tele=request.POST['tele'], message=request.POST['message'])
        return redirect('/contact?messagesent=message sent')


def products(request):
    categories = Category.objects.all()
    products = Article.objects.order_by('-id').all()
    # return HttpResponse(products[4].articleimages[0].name)

    # return JsonResponse(products[0]['ArticleImage'])

    return render(request, 'product/products.html',
                  {'products': products, 'swiper-bundle.Css': 'good', 'categories': categories})


def product(request, id):
    product = Article.objects.get(id=id)
    # return HttpResponse(Article.objects.first().SpecificationArticle.FinitionSpecification.all)
    categories = Category.objects.all()
    realtedproducts = Article.objects.filter(childcategory=product.childcategory)[0:6]
    dilevies = Delivery.objects.all()
    fileControles = FileControle.objects.all()
    datetimenow = str(datetime.datetime.now().strftime('%A %d %B'))
    if request.user.is_authenticated:
        displayexist = Pane.objects.filter(article_id=id, user=request.user).first()
        if displayexist:
            exist = True
        else:
            exist = False
    else:
        exist = False

    return render(request, 'product/product.html',
                  {'product': product, 'categories': categories, 'realtedproducts': realtedproducts,
                   'dilevies': dilevies, 'fileControles': fileControles, 'datetimenow': datetimenow, 'exist': exist})


def updatepanpage(request, id):
    exist = Pane.objects.filter(article_id=id, user=request.user).first()
    if exist:
        product = Article.objects.get(id=id)
        # return HttpResponse(Article.objects.first().SpecificationArticle.FinitionSpecification.all)
        categories = Category.objects.all()
        realtedproducts = Article.objects.filter(childcategory=product.childcategory)[0:6]
        dilevies = Delivery.objects.all()
        fileControles = FileControle.objects.all()
        datetimenow = str(datetime.datetime.now().strftime('%A %d %B'))
        displayexist = Pane.objects.filter(article_id=id, user=request.user).first()

        return render(request, 'product/modifyproduct.html',
                      {'product': product, 'categories': categories, 'realtedproducts': realtedproducts,
                       'dilevies': dilevies, 'fileControles': fileControles, 'datetimenow': datetimenow,
                       })
    else:
        return redirect('/product/' + str(id))


def productsbyCategory(request, category):
    categories = Category.objects.all()
    products = Article.objects.filter(childcategory__name=category).all()
    categoryid = ChildCategory.objects.filter(name=category).first().id
    CategoryHistory.objects.create(childcategory_id=categoryid)
    category = ChildCategory.objects.filter(name=category).first()
    return render(request, 'product/products.html',
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
    return render(request, 'product/searcharticle.html',
                  {'products': products, 'searchtitle': request.GET['rechercheinput'],
                   'categories': categories})


def onsearch(request):
    if request.method == 'POST':
        total = Specification.objects.first().minprice
        lists = Article.objects.filter(title__icontains=request.POST['searchtext']).values('id','title',
                                                                                           'articleimages__name',
                                                                                           'SpecificationArticle')[0:6]
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


def downloadpreparemyfile(request):
    return FileResponse(open('static/files/fileprepare.pdf', 'rb'))


def addtppan(request):
    if (request.method == 'POST'):
        ifexist = Pane.objects.filter(user=request.user, article_id=request.POST['articleid']).first()
        if ifexist:
            ifexist.delete()
        else:
            pane = Pane()
            pane.user = request.user
            pane.delevery_id = request.POST['delevery']
            pane.article_id = request.POST['articleid']
            pane.FileControle_id = request.POST['filecontrole']
            if 'mydesign' in request.POST:
                pane.ArticleDesign = request.FILES['mydesign']

            if 'format' in request.POST:
                pane.size_id = request.POST['format']

            if 'formatype' in request.POST:
                pane.formattype_id = request.POST['formatype']

            if 'papertype' in request.POST:
                pane.paperType_id = request.POST['papertype']

            if 'papercolor' in request.POST:
                pane.paperColor_id = request.POST['papercolor']

            if 'color' in request.POST:
                pane.fontColor_id = request.POST['color']

            if 'formadeplace' in request.POST:
                pane.side_id = request.POST['formadeplace']

            if 'orientation' in request.POST:
                pane.orientation_id = request.POST['orientation']

            if 'finitions' in request.POST:
                pane.finition_id = request.POST['finitions']

            if 'costumquantite' in request.POST:
                pane.CostumQuantity = request.POST['costumquantite']

            elif 'quantite' in request.POST:
                pane.Quantity_id = request.POST['quantite']
            pane.save()

        return redirect('/cart')
    else:
        return redirect('/')


def addfiletopane(request):
    if request.method == 'POST':
        # return JsonResponse(request.POST['file'])
        # pane = Pane.objects.get(id=request.POST['paneid'])
        # pane.ArticleDesign = request.POST['file']
        uploaded_file = request.FILES['file']
        default_storage.save(uploaded_file.name, uploaded_file)
        pane = Pane.objects.get(id=request.POST['paneid'], user_id=request.user.id)
        pane.ArticleDesign.delete()
        pane.ArticleDesign = uploaded_file
        pane.save()
        jsondata = [{'name': uploaded_file.name, 'size': uploaded_file.size}]
        return JsonResponse(jsondata, safe=False)
    else:
        return redirect('')


def deletefileuploaded(request):
    if request.method == 'POST':
        pane = Pane.objects.get(id=request.POST['deletepaneid'], user_id=request.user.id)
        pane.ArticleDesign.delete()
        return redirect('/cart')
    else:
        return redirect('/')


def updatepan(request):
    if (request.method == 'POST'):
        pane = Pane.objects.get(user=request.user, article_id=request.POST['articleid'])
        pane.delevery_id = request.POST['delevery']
        pane.FileControle_id = request.POST['filecontrole']
        if 'mydesign' in request.POST:
            pane.ArticleDesign = request.POST['mydesign']

        if 'format' in request.POST:
            pane.size_id = request.POST['format']

        if 'formatype' in request.POST:
            pane.formattype_id = request.POST['formatype']

        if 'papertype' in request.POST:
            pane.paperType_id = request.POST['papertype']

        if 'papercolor' in request.POST:
            pane.paperColor_id = request.POST['papercolor']

        if 'color' in request.POST:
            pane.fontColor_id = request.POST['color']

        if 'formadeplace' in request.POST:
            pane.side_id = request.POST['formadeplace']

        if 'orientation' in request.POST:
            pane.orientation_id = request.POST['orientation']

        if 'finitions' in request.POST:
            pane.finition_id = request.POST['finitions']

        if 'quantite' in request.POST:
            pane.Quantity_id = request.POST['quantite']

        pane.save()

    return redirect('/cart')


def duplicatepan(request):
    if request.method == 'POST':
        newpanel = Pane.objects.get(id=request.POST['cartid'], user=request.user)
        pane = Pane()
        pane.user = request.user
        pane.delevery_id = newpanel.delevery_id
        pane.article_id = newpanel.article_id
        pane.FileControle_id = newpanel.FileControle_id
        pane.ArticleDesign = newpanel.ArticleDesign
        pane.size_id = newpanel.size_id
        pane.formattype_id = newpanel.formattype_id
        pane.paperType_id = newpanel.paperType_id
        pane.paperColor_id = newpanel.paperColor_id
        pane.fontColor_id = newpanel.fontColor_id
        pane.side_id = newpanel.side_id
        pane.orientation_id = newpanel.orientation_id
        pane.finition_id = newpanel.finition_id
        pane.Quantity_id = newpanel.Quantity_id
        pane.save()
        return redirect('/cart')
    else:
        return redirect('/')


def deleteppan(request):
    if request.method == 'POST':
        Pane.objects.filter(id=request.POST['cartid'], user=request.user).delete()
        return redirect('/cart')


def cart(request):
    carts = Pane.objects.filter(user=request.user)
    # datetime.datetime.now()+datetime.timedelta
    total = 0
    for cart in carts:
        total += cart.total + cart.FileControle.price
    dilevies = Delivery.objects.all()
    total += dilevies.first().price
    datetimenow = str(datetime.datetime.now().strftime('%A %d %B'))
    return render(request, 'product/cart.html',
                  {'carts': carts, 'total': total, 'dilevies': dilevies, 'datetimenow': datetimenow})


def cartdeleveryprice(request):
    if request.method == "POST":
        delevery = Delivery.objects.get(id=request.POST['deleveryid'])
        carts = Pane.objects.filter(user=request.user)
        total = 0
        for cart in carts:
            total = total + cart.total
        total += delevery.price
        data = json.dumps({
            'mindate': str((datetime.datetime.now() + datetime.timedelta(days=delevery.mindays)).strftime('%A %d %B')),
            'maxdate': str((datetime.datetime.now() + datetime.timedelta(days=delevery.maxdays)).strftime('%A %d %B')),
            'price': delevery.price,
            'total': total
        })

        return HttpResponse(data, content_type='application/json')
    else:
        return redirect('/')


def deleveryfilter(request):
    if request.method == "POST":
        if 'finitions' in request.POST:
            finitionprice = int(Finition.objects.get(id=request.POST['finitions']).price)
            if finitionprice == 0:
                finitionprice = 1
        else:
            finitionprice = 1

        if 'papertype' in request.POST:
            papertypeprice = int(PaperType.objects.get(id=request.POST['papertype']).price)
            if papertypeprice == 0:
                papertypeprice = 1
        else:
            papertypeprice = 1

        delevery = Delivery.objects.get(id=request.POST['deleveryid'])

        quantite = float(request.POST['quantity'])
        deleveryprice = float(delevery.price)
        filecontroller = float(request.POST['filecontroller'])

        total = (finitionprice * papertypeprice * quantite) + deleveryprice + filecontroller
        data = json.dumps({
            'mindate': str((datetime.datetime.now() + datetime.timedelta(days=delevery.mindays)).strftime('%A %d %B')),
            'maxdate': str((datetime.datetime.now() + datetime.timedelta(days=delevery.maxdays)).strftime('%A %d %B')),
            'price': delevery.price,
            'total': total
        })

        return HttpResponse(data, content_type='application/json')
    else:
        return redirect('/')


def filecontrolefilter(request):
    if request.method == "POST":
        if 'finitions' in request.POST:
            finitionprice = int(Finition.objects.get(id=request.POST['finitions']).price)
            if finitionprice == 0:
                finitionprice = 1
        else:
            finitionprice = 1

        if 'papertype' in request.POST:
            papertypeprice = int(PaperType.objects.get(id=request.POST['papertype']).price)
            if papertypeprice == 0:
                papertypeprice = 1
        else:
            papertypeprice = 1

        filecontrole = FileControle.objects.get(id=request.POST['filecontroleid'])

        quantite = float(request.POST['quantity'])
        delevery = float(request.POST['delevery'])
        filecontrollerprice = filecontrole.price

        total = (finitionprice * papertypeprice * quantite) + delevery + filecontrollerprice

        data = json.dumps({
            'name': filecontrole.name,
            'price': filecontrole.price,
            'total': total
        })
        # return HttpResponse('good')
        return HttpResponse(data, content_type='application/json')
    else:
        return redirect('/')


def pricefilter(request):
    if request.method == 'POST':
        if 'finitions' in request.POST:
            finitionprice = int(Finition.objects.get(id=request.POST['finitions']).price)
            if finitionprice == 0:
                finitionprice = 1
        else:
            finitionprice = 1

        if 'papertype' in request.POST:
            papertypeprice = int(PaperType.objects.get(id=request.POST['papertype']).price)
            if papertypeprice == 0:
                papertypeprice = 1
        else:
            papertypeprice = 1

        quantite = float(request.POST['quantity'])
        delevery = float(request.POST['delevery'])
        filecontroller = float(request.POST['filecontroller'])

        total = (finitionprice * papertypeprice * quantite) + delevery + filecontroller
        return HttpResponse(str(total))
    else:
        return redirect('/')


def mes_commendes(request):
    commades = Commande.objects.filter(User=request.user).all()
    return render(request, 'profile/commandes.html', {'commades': commades})


def infoverify(request):
    return render(request, 'verify/infoverify.html')


def infoverifyclick(request):
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
        return redirect('/adresseverify')
    else:
        return redirect('/cart')


def adresseverify(request):
    return render(request, 'verify/adresseverify.html')


def adresseverifyclick(request):
    if (request.method == 'POST'):
        Client.objects.update_or_create(user_id=request.user.id,
                                        defaults={
                                            'adresse1': request.POST['adresse1'],
                                            'adresse2': request.POST['adresse2'],
                                            'codepostal': request.POST['codepostal'],
                                            'city': request.POST['ville'],
                                            'country': request.POST['pays']
                                        })
        return redirect('/livraisonverify')
    else:
        return redirect('/cart')


def livraisonverify(request):
    dilevies = Delivery.objects.all()
    fileControles = FileControle.objects.all()
    return render(request, 'verify/deleveryvirify.html', {'dilevies': dilevies, 'fileControles': fileControles})


def livraisondelevertverify(request):
    if request.method == "POST":
        delevery = Delivery.objects.get(id=request.POST['deleveryid'])
        data = json.dumps({
            'mindate': str((datetime.datetime.now() + datetime.timedelta(days=delevery.mindays)).strftime('%A %d %B')),
            'maxdate': str((datetime.datetime.now() + datetime.timedelta(days=delevery.maxdays)).strftime('%A %d %B')),
            'price': delevery.price,
        })

        return HttpResponse(data, content_type='application/json')
    else:
        return redirect('cart')


def livraisonfilecontroleverify(request):
    if request.method == "POST":
        filecontrole = FileControle.objects.get(id=request.POST['filecontroleid'])
        data = json.dumps({
            'name': filecontrole.name,
            'price': filecontrole.price,
        })
        # return HttpResponse('good')
        return HttpResponse(data, content_type='application/json')
    else:
        return redirect('cart')


def livraisonverifyclick(request):
    if request.method == 'POST':
        pane = Pane.objects.filter(user_id=request.user.id).update(delevery=request.POST['delevery'])
        return redirect('/commandeverify')
    else:
        return redirect('/cart')


def commandeverify(request):
    carts = Pane.objects.filter(user_id=request.user.id).all()
    total = 0
    for cart in carts:
        total = total + cart.total
    delevery = carts.first().delevery.price
    total += delevery
    return render(request, 'verify/commandeverify.html', {'carts': carts, 'total': total})


def commandeverifyclick(request):
    if request.method == 'POST':
        # carts = Pane.objects.filter(user_id=request.user.id).all()
        # total = 0
        # for cart in carts:
        #     total = total + cart.total
        # delevery = carts.first().delevery.price
        # total += delevery
        #
        # panes = Pane.objects.filter(user_id=request.user.id).all()
        # commande = Commande.objects.create(User=request.user, total=total, delevery=panes.first().delevery)
        # for pane in panes:
        #     commande.Pane.add(pane)
        #
        # body = render_to_string('mails/commandeMail.html',
        #                         {'user': request.user.username, 'carts': carts, 'total': total})
        # msg = EmailMessage('test', body, 'info@impresiion.com', ['del.souhaib@gmail.com'])
        # msg.content_subtype = "html"
        # msg.send()
        # return redirect('/mes_commendes')

        return redirect('/payementverify')
    else:
        return redirect('/')


def payementrequest():
    url = "https://test.oppwa.com/v1/checkouts"
    data = {
        'entityId': '8a8294174b7ecb28014b9699220015ca',
        'amount': '92.00',
        'currency': 'EUR',
        'paymentType': 'DB'
    }
    try:
        opener = build_opener(HTTPHandler)
        request = Request(url, data=urlencode(data).encode('utf-8'))
        request.add_header('Authorization', 'Bearer OGE4Mjk0MTc0YjdlY2IyODAxNGI5Njk5MjIwMDE1Y2N8c3k2S0pzVDg=')
        request.get_method = lambda: 'POST'
        response = opener.open(request)
        return json.loads(response.read())
    except HTTPError as e:
        return json.loads(e.read())
    except URLError as e:
        return e.reason


def payementverify(request):
    data = payementrequest()
    return render(request, 'verify/payementverify.html', {'checkoutid': data})


def payementstatutrequest(id, resourcePath):
    url = "https://test.oppwa.com/v1/checkouts/" + id + "/payment"
    url += '?entityId=8a8294174b7ecb28014b9699220015ca'
    try:
        opener = build_opener(HTTPHandler)
        request = Request(url, data=b'')
        request.add_header('Authorization', 'Bearer OGE4Mjk0MTc0YjdlY2IyODAxNGI5Njk5MjIwMDE1Y2N8c3k2S0pzVDg=')
        request.get_method = lambda: 'GET'
        response = opener.open(request)
        return json.loads(response.read())
    except HTTPError as e:
        return json.loads(e.read())
    except URLError as e:
        return e.reason


def payementstatut(request):
    responseData = payementstatutrequest(request.GET['id'], request.GET['resourcePath'])
    if responseData['result']['code'] == '000.100.110':
        carts = Pane.objects.filter(user_id=request.user.id).all()
        total = 0
        for cart in carts:
            total = total + cart.total
        delevery = carts.first().delevery.price
        total += delevery

        panes = Pane.objects.filter(user_id=request.user.id).all()
        commande = Commande.objects.create(User=request.user, total=total, delevery=panes.first().delevery)
        for pane in panes:
            commande.Pane.add(pane)

        body = render_to_string('mails/commandeMail.html',
                                {'user': request.user.username, 'carts': carts, 'total': total})
        msg = EmailMessage('test', body, 'info@impresiion.com', ['del.souhaib@gmail.com'])
        msg.content_subtype = "html"
        msg.send()
        return redirect('/mes_commendes?statut=sucess&&amount=' + responseData['amount'])
    else:
        return redirect(request.META.get('HTTP_REFERER') + '?statut=error')


def payementverifyclick(request):
    return redirect('/commandeverify')


def test(request):
    try:
        from urllib.parse import urlencode
        from urllib.request import build_opener, Request, HTTPHandler
        from urllib.error import HTTPError, URLError
    except ImportError:
        from urllib import urlencode
        from urllib2 import build_opener, Request, HTTPHandler, HTTPError, URLError
    import json

    def request():
        url = "https://test.oppwa.com/v1/checkouts"
        data = {
            'entityId': '8a8294174b7ecb28014b9699220015ca',
            'amount': '92.00',
            'currency': 'EUR',
            'paymentType': 'DB'
        }
        try:
            opener = build_opener(HTTPHandler)
            request = Request(url, data=urlencode(data).encode('utf-8'))
            request.add_header('Authorization', 'Bearer OGE4Mjk0MTc0YjdlY2IyODAxNGI5Njk5MjIwMDE1Y2N8c3k2S0pzVDg=')
            request.get_method = lambda: 'POST'
            response = opener.open(request)
            return json.loads(response.read())
        except HTTPError as e:
            return json.loads(e.read())
        except URLError as e:
            return e.reason

    responseData = request()
    return JsonResponse(responseData)
    return HttpResponse('good')
