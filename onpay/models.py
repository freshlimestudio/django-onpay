# coding: UTF-8
"""\
Модели для django-onpay

Интернационализации нет, так как сам onpay проект русский и я расчитываю,
что прикручивать его будут тоже русские программисты.
"""
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from onpay.conf import get_constant
from onpay.signals import refilled_balance

class Operation(models.Model):
    sum = models.DecimalField(verbose_name=u"сумма", max_digits=8, decimal_places=2)
    user = models.ForeignKey(User, verbose_name=u"пользователь", )
    status = models.BooleanField(verbose_name=u"оплачено", default=get_constant('new_operation_status'))
    type = models.CharField(max_length=64, verbose_name=u"тип", default=u"внешняя")
    comment = models.CharField(max_length=255, verbose_name=u"комментарий", default=u"Пополнение счета")
    description = models.CharField(max_length=255, verbose_name=u"описание", default=u"через систему Onpay")
    date = models.DateTimeField(verbose_name=u"дата", auto_now_add=True)

    class Meta:
        verbose_name = u"операция"
        verbose_name_plural = u"операции"

    def __unicode__(self):
        return u"id %d, sum %s, st %s" % (self.id, self.sum, self.status)

class Balance(models.Model):
    sum = models.DecimalField(verbose_name=u"сумма", max_digits=8, decimal_places=2)
    user = models.OneToOneField(User, verbose_name=u"пользователь", )
    date = models.DateTimeField(verbose_name=u"дата", auto_now_add=True)

    class Meta:
        verbose_name = u"баланс"
        verbose_name_plural = u"балансы"

    def __unicode__ (self):
        return u"%d, %s" % (self.id, self.sum)


def data_get_created_operation(id):
    "функция выборки неоплаченной операции по ID"
    return Operation.objects.get(id=id, status=get_constant('new_operation_status'))


def data_update_user_balance(operation_id, sum):
    """
    обновление баланса пользователя

    если параметр use_balance_table установлен в false, то этот метод не вызывается
    operation_id - ID в таблице operations, по нему можно получить ID пользователя
    """
    try:
        operation = data_get_created_operation(operation_id)
    except Operation.DoesNotExist:
        return False

    return refill(operation.user, sum)


def refill(user, sum):
    try:
        balance = Balance.objects.get(user=user)
        balance.sum += sum
        balance.save()
    except Balance.DoesNotExist:
        balance = Balance.objects.create(user=user, sum=sum)
    refilled_balance.send(sender=balance, user=user, sum=sum)
    return True

