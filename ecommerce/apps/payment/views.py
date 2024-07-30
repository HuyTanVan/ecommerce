import stripe
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ecommerce.apps.orders.views import payment_confirmation
from ecommerce.apps.basket.basket import Basket
# Create your views here.
@login_required
def view_payment(request):
    # No auth: 4242424242424242

    # Auth: 4000002500003155

    # Error: 4000000000009995
    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)

    stripe.api_key = 'sk_test_51POs4ZP6qrjtDGURbpOiNRKuPpUqrDvKVj6ZhNn8tb1Y093jACa6mLCIV1KhPDlSzcjAGKvm3gPvVWsROEQdnmX600rbibUn2R'
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='usd',
        metadata={'userid': request.user.id}
    )
    basket = Basket(request)
    
    return render(request, 'payment/payment_home.html', {'client_secret': intent.client_secret, 'basket': basket})
def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None
    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print("ERROR: ", e)
        return HttpResponse(status=400)
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)
    else:
        print('Unhandled event type {}'.format(event.type))
    return HttpResponse(status=200)
