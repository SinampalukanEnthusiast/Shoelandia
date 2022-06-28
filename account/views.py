from .token import account_activation_token
from .models import UserBase
from .forms import RegistrationForm
# from orders.views import user_orders
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout


@login_required
def dashboard(request):
    # orders = user_orders(request)
    return render(request, 'account/user/dashboard.html')


def account_register(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('registered succesfully and activation sent')
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('dashboard')
    else:
        return render(request, 'account/registration/activate_invalid.html')


# def register(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     else:
#         form = RegisterUser()
#         if request.method == 'POST':
#             form = RegisterUser(request.POST)
#             if form.is_valid():
#                 form.save()
#                 customer_username = form.cleaned_data['username']
#                 customer_name = f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}"
#                 email = form.cleaned_data['email']
#                 user = User.objects.get(username=customer_username)
#                 customer = Customer.objects.create(
#                     name=customer_name, email=email)
#                 customer.user = user
#                 customer.save()
#                 messages.success(request, "Account created!")
#                 return redirect('login')
#         context = {'form': form}
#         return render(request, 'store/register.html', context)
