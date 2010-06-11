#coding: utf-8
from django.dispatch import Signal
from django.core.mail import mail_admins, mail_managers

from onpay.conf import get_constant

refilled_balance = Signal(providing_args=["user", "sum"])

def update_balance(sender, **kw):
    "Пример пополнения баланса"
    kw['user'].footman_profile.money += kw['sum']
    kw['user'].footman_profile.save()

def email_notification(sender, **kw):
    mail_managers(
        subject=u"Money from %s" % kw['user'].username,
        message=u"Balance refilled for %s RUR" % kw['sum'],
    )

if get_constant("enable_footman_update_balance"):
    refilled_balance.connect(update_balance)

if get_constant("enable_email_notify"):
    refilled_balance.connect(email_notification)
