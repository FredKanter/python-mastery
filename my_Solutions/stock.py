# stock.py
import csv
from decimal import Decimal


class Stock:
    __slots__ = ('name', '_shares', '_price')
    _types = (str, int, float)
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @property
    def cost(self):
        return self.shares * self.price
    
    def sell(self, nshares):
        self.shares = self.shares - nshares

    @property
    def shares(self):
        return self._shares
    
    @shares.setter
    def shares(self, value):
        if not isinstance(value, self._types[1]):
            raise TypeError(f'Expected {self._types[1].__name__}')
        if value < 0:
            raise ValueError('Expected value >= 0')
        self._shares = value

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if not isinstance(value, self._types[2]):
            raise TypeError(f'Expected {self._types[2].__name__}')
        if value < 0:
            raise ValueError('Expected value >= 0')
        self._price = value

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)
    
    def __repr__(self) -> str:
        return f'Stock({self.name}, {self.shares}, {self.price})'
    
    def __eq__(self, other):
        same_attr = ((self.name, self.shares, self.price) == 
                     (other.name, other.shares, other.price))
        return isinstance(other, Stock) and same_attr
    
class DStock(Stock):
        _types = (str, int, Decimal)

'''
def read_portfolio(filename, types=[str, int, float], from_row=False):
    # Enable user to choose class
    available_classes = {'Stock': Stock,
                         'DStock': DStock}
    which_class = input(f"Choose a class from {list(available_classes.keys())}: ")
    wcls = available_classes[which_class]

    portfolio = []
    with open(filename) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
     
        for row in f_csv:
            if from_row:
                portfolio.append(wcls.from_row(row))
            else:
                portfolio.append(wcls(*(func(entry) for func, entry in zip(types, row))))
    return portfolio
'''

def print_portfolio(portfolio, headers=('name', 'shares', 'price')):
    # print headers
    print('%10s %10s %10s' % headers)
    print(10*'-'+' '+10*'-'+' '+10*'-')

    for s in portfolio:
           print('%10s %10d %10.2f' % (s.name, s.shares, s.price))