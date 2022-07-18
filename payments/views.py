import stripe

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    return render(request, 'payments/home.html')


def signup(request):
    if request.method == 'POST':
        _ = User.objects.create_user(username=request.POST['email'], email=request.POST['email'], password=request.POST['password'])
        return HttpResponseRedirect(reverse('login'))

    return render(request, 'payments/signup.html')


def signin(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('checkout'))

        return HttpResponse('Invalid credentials')

    return render(request, 'payments/login.html')


@login_required
@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email=request.user.email,
                payment_method_types=['card'],
                line_items=[{
                    'price': settings.STRIPE_PRICE_ID,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"http://{request.META['HTTP_HOST']}{reverse('message')}?message=success",
                cancel_url=f"http://{request.META['HTTP_HOST']}{reverse('message')}?message=cancelled",
            )
            return JsonResponse({'id': checkout_session.id})

        except Exception as e:
            print('error: ', str(e))
            return HttpResponse(str(e))

    return HttpResponse('Only POST requests')


@login_required
def show_message(request):
    return HttpResponse(request.GET.get('message', ''))


@login_required
def checkout(request):
    return render(request, 'payments/checkout.html', {'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY})


@login_required
def manage_billing(request):
    session = stripe.billing_portal.Session.create(
        customer='cus_J8C20GxZyUtC7a',
        return_url=f'http://{request.META["HTTP_HOST"]}{reverse("checkout")}',
    )
    return HttpResponseRedirect(session.url)