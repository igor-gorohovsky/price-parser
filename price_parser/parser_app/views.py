from django.shortcuts import render
from django.http import HttpResponse

from .models import Urls


def index(request):
    urls = Urls.objects.all()
    return render(
        request,
        'parser_app/index.html',
        context={'urls': urls, 'title': 'Rozetka Parser'},
    )
