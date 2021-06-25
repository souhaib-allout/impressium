from django.db.models import Count

from clientside.models import *


def globaldata(request):
    bestarticles = Article.objects.filter(bestarticle__id__isnull=False)
    topcategories = CategoryHistory.objects.values('childcategory', 'childcategory__name').annotate(
        nb_search=Count('childcategory_id')).order_by('childcategory_id')[0:8]
    categories = Category.objects.all()
    nbpanes=Pane.objects.filter(user=request.user).all()
    return {'bestarticles': bestarticles, 'topcategories': topcategories,
                   'categories': categories,'nbpanes':nbpanes}
