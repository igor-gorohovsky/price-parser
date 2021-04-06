from django.urls import path

from . import views


urlpatterns = [
    path('', views.HomeProductList.as_view(), name='index'),
    path('product_info/<int:pk>', views.ProductView.as_view(), name='info'),
    path('archive', views.ArchiveProductList.as_view(), name='archive'),
    path('cabinet', views.cabinet, name='cabinet'),
]
