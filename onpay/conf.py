# coding: UTF-8

from django.conf import settings

def get_constant(name, default=None):
    return settings.ONPAY.get(name, default)

# error codes (not used)
OK = 0
NO_CONNECTION = 1
INCORRECT_MD5 = 8
ORDER_NOT_FOUND = 10
BAD_PAY_FOR = 11
ERROR_PARAMETERS = 12
