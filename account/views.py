# from .token import account_activation_token
from email.headerregistry import Address
from pickle import TRUE

from django.urls import reverse
from .models import Addresses, Customer
from .forms import AddressForm, RegistrationForm, LoginForm, DashboardEditForm
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from orders.models import Order


@login_required
def dashboard(request):
    # orders = user_orders(request)
    return render(request, 'account/user/dashboard.html')


@login_required
def dashboard_edit(request):
    if request.method == 'POST':
        user_form = DashboardEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Details updated successfuly!")
    else:
        user_form = DashboardEditForm(instance=request.user)

    return render(request,
                  'account/user/dashboard_edit.html', {'form': user_form})


def orders(request):

    customer = request.user.id
    orders = Order.objects.filter(user_id=customer)
    print(orders)
    context = {'orders': orders}
    return render(request, "account/user/orders.html", context)


@login_required
def delete_user(request):
    user = Customer.objects.get(name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('delete_confirm')


def account_register(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = True
            user.save()
            # current_site = get_current_site(request)
            # subject = 'Activate your Account'
            # message = render_to_string('account/registration/activate_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            # user.email_user(subject=subject, message=message)
            return redirect('dashboard')
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


def account_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Account logged in!")
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect!')
        context = {'form': LoginForm()}
        return render(request, 'account/registration/login.html', context)


@login_required
def addresses(request):
    addresses = Addresses.objects.filter(
        customer=request.user)
    print(addresses)
    context = {'addresses': addresses}
    return render(request, 'account/user/addresses.html', context)


def add_address(request):
    if request.method == 'POST':
        address_form = AddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            messages.success(request, 'Address added!')
            prev_url = request.META.get("HTTP_REFERER")
            # if "delivery_address" in prev_url:
            #     return redirect("delivery_address")
            return HttpResponseRedirect(prev_url)
    else:
        address_form = AddressForm()
        # for item in address_form:
        #     print(item)

    context = {'form': address_form}

    return render(request, 'account/user/address_edit.html', context)


def edit_address(request, id):
    if request.method == 'POST':
        address = Addresses.objects.get(pk=id, customer=request.user)
        address_form = AddressForm(instance=address, data=request.POST)

        if address_form.is_valid():
            address_form.save()
            messages.success(request, 'Address edited!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        address = Addresses.objects.get(pk=id, customer=request.user)
        address_form = AddressForm(instance=address,)

    context = {'form': address_form}

    return render(request, 'account/user/address_edit.html', context)


def delete_address(request, id):
    address = Addresses.objects.filter(pk=id, customer=request.user).delete()
    messages.success(request, 'Address deleted successfuly!')
    return redirect('addresses')


def set_default(request, id):
    address = Addresses.objects.filter(
        customer=request.user, default=True).update(default=False)
    address = Addresses.objects.filter(
        customer=request.user, pk=id).update(default=True)
    messages.success(request, 'Address set default successfuly!')
    prev_url = request.META.get("HTTP_REFERER")
    if "delivery_address" in prev_url:
        return redirect("delivery_address")
    return redirect('addresses')
