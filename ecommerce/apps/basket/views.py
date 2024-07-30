from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from decimal import Decimal
# class import
from ecommerce.apps.store.models import Product
from .basket import Basket

# Create your views here.
def basket_summary(request):
    basket = Basket(request)
    
    return render(request, 'store/basket/summary.html', {'basket': basket})    
def basket_add(request):
    basket = Basket(request=request)   
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_price = str(request.POST.get('productprice'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        
        basket.add(product=product,price=product_price, qty=product_qty)
    
        basketqty = basket.__len__() 
        response = JsonResponse({'qty': basketqty})
    
        return response
def basket_delete(request):
    basket = Basket(request=request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)
        
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response
def basket_update(request):
    basket = Basket(request=request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        item_total = basket.get_itemtotal_price(product=product_id)
        basket.update(product=product_id, qty=product_qty)
        
        basket_qty =  basket.__len__()
        basket_total = basket.get_subtotal_price()

        json_response = JsonResponse({'itemtotal': item_total, 'qty': basket_qty, 'subtotal': basket_total})
        return json_response