

from decimal import Decimal
from math import prod
from store.models import Product


class Basket():
    def __init__(self, request):

        self.session = request.session

        basket = self.session.get('skey')

        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, qty):
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product_id), 'qty': qty}

        self.save()

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        # sum = 0

        # for item in self.basket.values():
        #     sum += item['qty']
        # #print(f'len: {sum}')
        return sum(item['qty'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def delete(self, product):
        product_id = str(product)
        print(f'product id: {product} \nself.basket: {self.basket}')
        if product_id in self.basket:
            del self.basket[product_id]
            print("deleted successfully")
            self.save()

    def update(self, product, qty):
        product_id = str(product)
        product_qty = qty
        if product_id in self.basket:
            self.basket[product_id]['qty'] = product_qty
        self.save()

    def save(self):
        self.session.modified = True
