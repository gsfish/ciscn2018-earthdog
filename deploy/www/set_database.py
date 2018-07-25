#!/usr/bin/env python

import os
import sys
import string
import random

import django


os.environ["DJANGO_SETTINGS_MODULE"] = "www.settings"
django.setup()
FRUITS_LIST = ['TOMATO', 'PINEAPPLE', 'WATERMELON', 'BANANA', 'SHADDOCK', 'ORANGE', 'APPLE', 'LEMON', 'CHERRY', 'PEACH', 'EAR', 'COCONUT', 'STRAWBERRY', 'RASPBERRY', 'BLUEBERRY', 'BLACKBERRY', 'GRAPE', 'MANGO', 'APRICOT', 'NECTARINE', 'PERSIMMON', 'POMEGRANATE', 'JACKFRUIT', 'CUMQUAT', 'LITCHI', 'GREENGAGE', 'HAW', 'PLUM', 'LONGAN', 'STARFRUIT', 'LOQUAT', 'TANGERINE', 'GUAVA']


def create(num):
    from www import settings
    from sshop.models import Commodity


    commodity_list = []
    for _ in range(num):
        name = '{0}_{1}'.format(random.choice(FRUITS_LIST), ''.join(random.sample(string.ascii_letters, 5)))
        desc = 'can you afford me? :D'
        price = random.randint(settings.INIT_PRICE_MIN, settings.INIT_PRICE_MAX)
        commodity_list.append(Commodity(name=name, desc=desc, price=price))
    Commodity.objects.bulk_create(commodity_list)
    print('[+] {0} commoditys created'.format(num))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('[-] usage: python {0} {1}'.format(sys.argv[0], 100))
        exit(0)
    else:
        create(int(sys.argv[1]))
