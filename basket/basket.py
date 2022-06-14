

from decimal import Decimal
from math import prod
from store.models import Product


class Basket():
    """
    Initialize a basket class, 
    associate it with the browser session
    """

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
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}

        print(self.basket)
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
        """
        The oneliner is equivalent to
        sum = 0
        for item in self.basket.values():
            sum += item['qty']
        retun sum

        Returns:
            This returns the number of items in a basket
        """
        return sum(item['qty'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def delete(self, product):
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def update(self, product, qty):
        product_id = str(product)
        product_qty = qty
        if product_id in self.basket:
            self.basket[product_id]['qty'] = product_qty
        self.save()

    def save(self):
        self.session.modified = True
