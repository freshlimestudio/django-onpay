# coding: UTF-8
from hashlib import md5

from django import forms

from onpay.conf import get_constant

class OnpayForm(forms.Form):
    sum = forms.DecimalField(label=u"Сумма")

class OnpayPayForm(forms.Form):
    type = forms.CharField()
    onpay_id = forms.IntegerField()
    pay_for = forms.IntegerField()
    amount = forms.DecimalField()
    order_amount = forms.DecimalField()
    order_currency = forms.CharField(max_length=4)
    balance_amount = forms.DecimalField()
    balance_currency = forms.CharField(max_length=4)
    exchange_rate = forms.DecimalField()
    paymentDateTime = forms.CharField()
    md5 = forms.CharField(max_length=32)
    note = forms.CharField(required=False)
    user_email = forms.CharField(required=False)

    def check_md5(self):
        u"Check hash strings"
        array = (self.cleaned_data['type'], self.cleaned_data['pay_for'],
            self.cleaned_data['onpay_id'], self.cleaned_data['order_amount'],
            self.cleaned_data['order_currency'], get_constant('private_code'))
        md5fb = md5(";".join(str(o_0) for o_0 in array)).hexdigest().upper()
        return self.cleaned_data["md5"] == md5fb

