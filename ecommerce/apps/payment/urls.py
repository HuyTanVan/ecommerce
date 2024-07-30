from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'payment'
urlpatterns = [
    path('', views.view_payment, name='view_payment'),
    path('orderplaced/', views.order_placed, name='order_placed'),
    path(r'webhook/', views.stripe_webhook)
]
