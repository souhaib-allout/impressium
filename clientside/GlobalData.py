from django.db.models import Count

from clientside.models import *


def globaldata(request):
    bestarticles = Article.objects.filter(bestarticle__id__isnull=False)
    topcategories = CategoryHistory.objects.values('childcategory', 'childcategory__name').annotate(
        nb_search=Count('childcategory_id')).order_by('childcategory_id')[0:8]
    categories = Category.objects.all()
    allptoducts = Article.objects.all().order_by('title')
    if (request.user.is_authenticated):
        nbpanes = Pane.objects.filter(user=request.user).all()
    else:
        nbpanes = 0
    closediv = '</div>'
    div = '<div>'
    return {'bestarticles': bestarticles, 'topcategories': topcategories,
            'categories': categories, 'nbpanes': nbpanes, 'allptoducts': allptoducts}


def chart(request):
    userschart = User.objects.values('date_joined__date', count=Count('*')).annotate(
        Count('date_joined__day')).order_by('date_joined__day')
    productchart = LastPane.objects.values('article__title').annotate(count=Count('article__id'))[0:7]
    categorieschart = CategoryHistory.objects.values('childcategory__name').annotate(
        count=Count('childcategory__id'))[0:7]
    # return HttpResponse(categorieschart)
    return {'userschart': userschart, 'productchart': productchart, 'categorieschart': categorieschart}
