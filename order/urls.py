from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home_view, name='home_view'),
    path('order/', views.add_order, name='order_view'),
    path('list/', views.order_list, name='list_view'),
]
