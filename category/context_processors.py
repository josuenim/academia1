from .models import Categorias

def menu_links(request):
    links=Categorias.objects.all()
    return dict(links=links)