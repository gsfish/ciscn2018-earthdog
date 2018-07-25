import string
import random

from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password


class Commodity(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    desc = models.CharField(max_length=100, default='no description')
    amount = models.IntegerField(default=settings.INIT_INTEGRAL)
    price = models.FloatField(null=False, blank=False)

    def __str__(self):
        return '<Commodity: {0}>'.format(self.name)
    
    def sell(self, num):
        res = self.amount
        res -= num
        if res >= 0:
            self.amount = res
            return True
        else:
            return False


class User(models.Model):
    username = models.CharField(max_length=50)
    mail = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    integral = models.FloatField(default=1000)
    invited = models.IntegerField(default=0)

    def __str__(self):
        return '<User: {0}>'.format(self.username)

    def validate(self, password):
        return check_password(password, self.password)

    def set_pass(self, password):
        salt = ''.join(random.sample(string.ascii_letters, 6))
        self.password = make_password(password, salt)

    def pay(self, num):
        res = self.integral
        res -= num
        if res >= 0:
            self.integral = res
            return True
        else:
            return False


class Owner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)


class Flag(models.Model):
    key = models.CharField(max_length=100)

    def __str__(self):
        return 'Congratulations! {0}'.format(self.key)
