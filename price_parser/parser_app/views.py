from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .forms import UrlsForm
from .models import Urls


class HomeProductList(ListView):
    model = Urls
    template_name = 'parser_app/product_list.html'
    context_object_name = 'urls'

    def get_queryset(self):
        return Urls.objects.filter(archive=False)


class ArchiveProductList(ListView):
    model = Urls
    template_name = 'parser_app/product_list.html'
    context_object_name = 'urls'

    def get_queryset(self):
        return Urls.objects.filter(archive=True)


class ProductView(DetailView):
    model = Urls
    template_name = 'parser_app/product_info.html'
    context_object_name = 'url'


def cabinet(request):
    if request.method == 'POST':
        pass
    else:
        form = UrlsForm()
    return render(
        request,
        'parser_app/cabinet.html',
        context={'form': form},
    )
