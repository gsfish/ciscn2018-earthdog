#!/usr/bin/env python

import os
import sys
import string
import random

import django

from www import settings


os.environ["DJANGO_SETTINGS_MODULE"] = "www.settings"
django.setup()


def create_admin():
    from sshop.models import User


    User.objects.filter(username=settings.INIT_ADMIN_USER).delete()
    raw_pass = ''.join(random.sample(string.ascii_letters+string.digits, 20))
    admin = User(username=settings.INIT_ADMIN_USER, mail=settings.INIT_ADMIN_MAIL)
    admin.set_pass(raw_pass)
    admin.save()
    print('[+] admin created')


if __name__ == '__main__':
    create_admin()
