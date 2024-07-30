from decimal import Decimal,ROUND_HALF_UP

from ecommerce.apps.store.models import (Product, Inventory)
class Basket():
    def __init__(self, request):
        self.session = request.session
        basket =  self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket # => {'4': {'price': '1270.00', 'qty': 1}, '3': {'price': '675.99', 'qty': 4}}
        for item in basket:
            print(type(Product.objects.get(pk=item)))
    def __iter__(self):
        """ Collect pro_id in the session data to query the DB to return products """
        product_ids = self.basket.keys() # => dict_keys(['2', '1'])

        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]['product'] = product
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            
            yield item
    def add(self, product, price, qty):
        """ 
        Adding and updating the users basket session data 
        """
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(price), 'qty': int(qty)}
        self.save()
        print(sum(item['qty'] for item in self.basket.values()))
    def update(self, product, qty):
        """
        Delete values in session data 
        """
        product_id = str(product)
        product_qty = str(qty)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()
    def delete(self, product):
        product_id = str(product)
        print(product_id)
        if product_id in self.basket:
            del self.basket[product_id]
        self.save()
    def get_itemtotal_price(self, product):
        product_id = str(product)
        item_qty = int(self.basket[product_id]['qty'])
        item_price = Decimal(self.basket[product_id]['price'])
        return Decimal(item_qty * item_price)
        
    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def get_total_price(self):

        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

        if subtotal == 0:
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(11.50)

        total = subtotal + Decimal(shipping)
        return total
    def clear(self):
        del self.session['skey']
        self.save()
    def __len__(self):
        """
        length of the basket
        """
        return sum(item['qty'] for item in self.basket.values())
    def save(self): 
        """
        Tell django backend session there is a modification
        """
        self.session.modified = True