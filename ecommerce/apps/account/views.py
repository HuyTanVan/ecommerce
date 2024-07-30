from django.contrib.auth import login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import send_mail

from .models import (Customer, Address)
from ecommerce.apps.orders.models import (Order, OrderItem)
from .tokens import account_activation_token
from .forms import (RegistrationForm,
                    UserLoginForm,
                      PwdResetRequestForm,
                        PwdResetCustomForm,
                          UserAddressForm) # user-defined class
# Create your views here.
@login_required
def dashboard(request):
    if request.user.is_superuser:
        logout(request)
        return HttpResponse("Invalid")
    return render(request,
                  'accounts/dashboard/dashboard.html')
def edit_details(request):
    pass
# we cannot access any data or method from the forms.py, until we check if the form is valid
# Password Reset
def request_reset_password(request):
    resetForm = PwdResetRequestForm(request.POST)
    if request.user.is_authenticated:
        return redirect('account:dashboard')
    if request.method == 'POST':
        resetForm = PwdResetRequestForm(request.POST)
        if resetForm.is_valid():
            email = resetForm.clean_email()
            user = Customer.objects.get(email=email)
            message = render_to_string('accounts/user/password_reset_email.html', {
                    'user': Customer.objects.get(email=email),
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
            subject = 'Reset your password'       
            send_mail(subject,
                    message,
                    'admin2002@gmail.com', 
                    [email],
                    fail_silently=False,) 
            return HttpResponse('Password reset request is successful. Please check your email')
    return render(request, 'accounts/user/password_reset_request.html', {'form': resetForm})
def confirm_reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except():
        pass
    if user is not None and account_activation_token.check_token(user, token):
        pwdForm = PwdResetCustomForm(user, request.POST or None)
        if request.method == 'POST':
            if pwdForm.is_valid() and pwdForm.clean_new_password2() is not None:
                # if new pass = old passa => unsuccessful reset.  
                if pwdForm.check_old_password():
                    return render(request, 'accounts/user/password_reset_form.html', {'form': pwdForm})
                else:
                    pwdForm.save()
                    return render(request, 'accounts/user/reset_password_successful.html')
            else:          
                return render(request, 'accounts/user/password_reset_form.html', {'form': pwdForm})
        else:
            return render(request, 'accounts/user/password_reset_form.html', {'form': pwdForm})

    else:
        return HttpResponse('INVALID USER')









# LOGIN
def login_user(request):
    # if user login -> login page is not allowed to access
    if request.user.is_authenticated:
        return redirect('account:dashboard')
    if request.method == 'POST':
        authForm = UserLoginForm(request.POST)
        # if the form is valid and return email and password -> correct
        if authForm.is_valid() and authForm.clean() is not None:
            print(authForm.clean().get('email'))
            # check user status
            user = Customer.objects.get(email=authForm.clean().get('email'))
            if user.is_active:
                login(request, user)
                return redirect('account:dashboard')
            else:
                active_user(request, user.email)
                return HttpResponse('registered succesfully and activation sent')
        else:
            return HttpResponseRedirect(reverse('account:login'))
    else:        
        return render(request, 'accounts/registration/login.html',{'form': UserLoginForm})
# If user created an account but they did not activate it   
def active_user(request, email):
    user = Customer.objects.get(email=email)
    current_site = get_current_site(request)
    subject = 'Activate your Account'
    message = render_to_string('accounts/registration/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
    send_mail(subject,
            message,
            'l@1.com',
            [email],
            fail_silently=False,)
# SIGN UP
def account_register(request):
    # get the request from user -> using POST method to post it up to database
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST) # this form will print a html code
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()

            # Setup email 
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('accounts/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('registered succesfully and activation sent')
    else:
        registerForm = RegistrationForm()
    return render(request, 'accounts/registration/register.html', {'form': registerForm})
def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except():
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'accounts/registration/activation_invalid.html')
# Orders
@login_required
def view_orders(request):
    orders = {}
    order_objs = Order.objects.filter(user_id=request.user)

    for order in order_objs:  
        order_items = OrderItem.objects.filter(order_id=order)

        # orders.update({order: {'product': [str(item) for item in order_items], 'qty': [item.quantity for item in order_items]}})
        orders.update({order: zip([str(item) for item in order_items], [item.quantity for item in order_items])})
    print(orders.values())
    return render(request, 'accounts/dashboard/view_orders.html', {'orders': orders})
# Address
@login_required
def view_address(request):
    adddress = Address.objects.filter(customer=request.user)
    return render(request, 'accounts/dashboard/addresses.html', {'addresses': adddress})

@login_required
def add_address(request):
    if request.method == 'POST':
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm()
    return render(request, 'accounts/dashboard/edit_address.html', {"form": address_form})
@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, customer=request.user)
    
    if not address.get().default:
        error_message = None
        address.delete()
    return redirect("account:addresses")
@login_required
def edit_address(request):
    if request.method == 'POST':
        pass
    else:
        address_form = UserAddressForm()
@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)
    return redirect("account:addresses") 

