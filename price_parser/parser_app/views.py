from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

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


class CreateUrl(CreateView):
    model = Urls
    form_class = UrlsForm
    template_name = 'parser_app/create_url.html'

    def post(self, request):
        f = self.form_class(request.POST)

        if f.is_valid():
            for url in f.cleaned_data['url']:

                # Save url to db if it does not exist
                URL = self.model(url=url)
                if not self.model.objects.filter(url=url).exists():
                    URL.save()
            return redirect(reverse_lazy('index'))
        return render(request, self.template_name, {'form': f})
