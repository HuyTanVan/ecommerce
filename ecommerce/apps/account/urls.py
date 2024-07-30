from django.urls import path
from django.contrib.auth import views as auth_views
from ecommerce import settings
from . import views
# from .forms import (UserLoginForm)
app_name = 'account'

urlpatterns = [ path('register/', views.account_register, name='register'),
               path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
                                    # not built-in login 
               path('login/', views.login_user, name='login'),
                                                            
               path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
               path('password_reset/', views.request_reset_password, name='password_reset'),
               path('password_reset/password_reset_confirm/<uidb64>/<token>/', views.confirm_reset_password , name='password_reset_confirm'),                                            
               # user dashboard
               path('dashboard/', views.dashboard, name='dashboard'),
               path('orders', views.view_orders, name='view_orders'),
               path('addresses/', views.view_address, name='addresses'),
               path('addresses/add/', views.add_address, name='add_address'),
               path('addresses/edit/<slug:id>', views.edit_address, name='edit_address'),
               path('addresses/delete/<slug:id>', views.delete_address, name='delete_address'),
               path('addresses/set_default/<slug:id>', views.set_default, name='set_default'),




               ]
