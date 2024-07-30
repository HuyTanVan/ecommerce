from django import forms
from .models import (Customer, Address)
from  django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm)
from django.utils.translation import gettext_lazy as _
# class UserLoginForm(forms.Form):
#     email = forms.CharField(widget=forms.EmailInput(
#                                 attrs={'type': 'email', 'class':'form-control form-control-lg','id':'form3Example3', 
#                                 'placeholder':'Enter a valid email address'
#                             }))
#     password = forms.CharField(widget=forms.PasswordInput(
#                             attrs={'type': 'password',  'class':'form-control form-control-lg','id':'form3Example4',
#                             'placeholder':'Enter password'
#                             }))
class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
                            attrs={'type': 'email',
                                   'class':'form-control form-control-lg',
                                   'id':'form3Example3', 
                                   'placeholder':'Enter a valid email address'
                             }))
    password = forms.CharField(widget=forms.PasswordInput(
                            attrs={'type': 'password',
                                   'class':'form-control form-control-lg',
                                   'id':'form3Example4',
                                   'placeholder':'Enter password'
                             }))
    error_messages = 'Email or Password is NOT correct'
    active_error_message = 'Your account is not activated. Please Click it to activate your account.'
    # error_messages = {
    #     "invalid_login": _(
    #         "Please enter a correct %(username)s and password. Note that both "
    #         "fields may be case-sensitive."
    #     ),
    #     "inactive": _("This account is inactive."),
    # }
    class Meta:
        model = Customer
        fields = ('email',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class':'form-control form-control-lg',
                                   'id':'form3Example3', 
                                   'placeholder':'Enter a valid email address'})
        self.fields['password'].widget.attrs.update(
            {'class':'form-control form-control-lg',
                                   'id':'form3Example4',
                                   'placeholder':'Enter password'})
        
    # this function collects data from the form
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        
        if Customer.objects.filter(email=email).exists() and password:
            user = Customer.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
        else:
            raise forms.ValidationError(self.error_messages)
        
class RegistrationForm(forms.ModelForm):
    error_messages = {'required': 'Invalid'}
    user_name = forms.CharField(label='Username', min_length=4, max_length=50,
                                 help_text='Required', error_messages=error_messages)
    email = forms.EmailField(max_length=100, help_text='Required',
                                 error_messages=error_messages)
    password = forms.CharField(label='Password', widget=forms.PasswordInput,
                                 help_text='Password should contain letters, digits and special characters',
                                 error_messages=error_messages)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput,
                                 error_messages=error_messages)

    class Meta:
        model = Customer
        fields = ('user_name', 'email',)
    def clean_user_name(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = Customer.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        
        return user_name
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']
    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'That email is already taken. Try another.')
        return email
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control form-control-lg', 'id': 'form3Example1cg','type':' text', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control form-control-lg', 'id': 'form3Example3cg', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control form-control-lg', 'id': 'form3Example4cg', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control form-control-lg', 'id': 'form3Example4cdg', 'placeholder': 'Repeat Password'})
class PwdResetRequestForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email', 'id': 'email', 'placeholder':'name@example.com'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = Customer.objects.filter(email=email)
        if not user:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email
class PwdResetCustomForm(forms.Form):
    """
    A form that lets a user set their password without entering the old
    password
    """
    error_messages = None
    # error_messages = {
    #     "password_mismatch": _("The two password fields didn’t match."),
    #     "password_match": _("New password matches the old password. Please use another."),
    # }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        # help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    new_pass = None
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            self.error_messages = 'New password did not match. Please try again.'
            raise forms.ValidationError(
                self.error_messages
            )
        # password_validation.validate_password(password2, self.user)
        self.new_pass = password2
        return self.new_pass
    def check_old_password(self):
        status = self.user.check_password(self.new_pass)  
        if status:
            self.error_messages = 'New password matches the old password. Please try another.'
            raise forms.ValidationError(
                self.error_messages
            )
        return status
    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line", "address_line2", "city", "state", "zipcode", "delivery_instructions"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["phone"].widget.attrs.update({"class": "form-control mb-2 account-form", "placeholder": "Phone"})
        self.fields["address_line"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Address Line 1"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Optional"}
        )
        self.fields["city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "City"}
        )
        self.fields["state"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "State"}
        )
        self.fields["zipcode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "ZIP Code"}
        )
        self.fields["delivery_instructions"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Delivery instructions"}
        )