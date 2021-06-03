from decimal import *

dec = Decimal(5.343)

print(dec)

getcontext().prec = 3

dec = Decimal(3.4543534543)

print(dec)