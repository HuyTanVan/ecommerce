from django.shortcuts import render
from django.http.response import JsonResponse
import random
from ecommerce.apps.basket.basket import Basket
from ecommerce.apps.orders.models import (Order, OrderItem)
from ecommerce.apps.payment.models import (PaymentDetail, PaymentStatus, PaymentMethod)

def create_payment(total_paid, user_id, payment_key) -> PaymentDetail:
    payment = PaymentDetail.objects.create(amount=total_paid,
                                            customer=user_id,
                                              payment_key=payment_key,
                                              payment_method=PaymentMethod.objects.get(pk=1),
                                              status = PaymentStatus.objects.get(pk=1))
    return payment
def add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        user_id = request.user
        # order_key = pi_3PXYB2P6qrjtDGUR0fRxoy38_secret_EoN0bl6RuxQyElnePDa6xDkjf
        order_key = request.POST.get('order_key').split('_')[0:2]
        # intent_key = pi_3PXYB2P6qrjtDGUR0fRxoy38
        intent_key = order_key[0] + '_' + order_key[1]
        basket_total = basket.get_total_price()
        
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            # Payment intent is created first => create an Order
            payment_key_obj = create_payment(user_id=user_id, payment_key=intent_key, total_paid=basket_total)
            order = Order.objects.create(order_key=random.randint(100000, 999999),
                                          user_id=user_id,
                                          payment_key=payment_key_obj,
                                          total_paid=basket_total,
                                          )

            for item in basket:
                # print("PRODUCT----------------", item)
                # product = Product.objects.get(id=item)
                
                OrderItem.objects.create(order_id=order, product_id=item['product'], quantity=item['qty'])

        response = JsonResponse({'success': 'Return something'})
        print(response)
        return response
def payment_confirmation(data):
    Order.objects.filter(order_key=data)
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id)
    return orders
