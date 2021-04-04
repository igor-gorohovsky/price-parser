from django.shortcuts import render
from django.http import HttpResponse

from .models import Urls


def index(request):
    urls = Urls.objects.filter(archive=False)
    return render(
        request,
        'parser_app/index.html',
        context={'urls': urls},
    )

def product_info(request, product_id):
    urls = Urls.objects.all()
    return render(
        request,
        'parser_app/product_info.html',
        context={'urls': urls},
    )

def archive(request):
    urls = Urls.objects.filter(archive=True)
    return render(
        request,
        'parser_app/index.html',
        context={'urls': urls},
    )
