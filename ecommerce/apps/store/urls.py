from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [ path('', views.all_products, name='all_products'), 
                path(r'item/<slug>?P<sku>[-\w]+/$', views.product_detail, name='product_detail'),
                path('search/<slug:category_slug>/', views.category_list, name='category_list'),
                path('search/', views.search_engine, name='search_engine')
               ]
