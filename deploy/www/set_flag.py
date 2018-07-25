#!/usr/bin/env python

import os
import sys

import django


os.environ["DJANGO_SETTINGS_MODULE"] = "www.settings"
django.setup()


def change(flag):
    from sshop.models import Flag

    
    Flag.objects.all().delete()
    Flag.objects.create(key=flag)
    print('[+] flag changed')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('[-] usage: python {0} {1}'.format(sys.argv[0], 'CISCN{xxxxxxxflag}'))
        exit(0)
    else:
        change(sys.argv[1])
