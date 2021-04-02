from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('product_info/<int:product_id>', views.product_info, name='info'),
]
