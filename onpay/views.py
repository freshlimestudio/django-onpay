# coding: utf-8
from django.db.models import Q, F
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.simple import direct_to_template
from django.core.mail import mail_admins

import onpay.forms
import onpay.models
from onpay.conf import get_constant
from onpay.common import IframeGenerator, answer, answerpay
from onpay.common import answer_dict, answerpay_dict

iframe_generator = IframeGenerator()

@login_required
def process_first_step(request, template_name="onpay/form.html",
                       iframe_template_name="onpay/iframe.html",
                       extra_context=None):
    Form = onpay.forms.OnpayForm
    form = Form(request.POST) if request.method == "POST" else Form()
    if request.method == "POST" and form.is_valid():
        op_id = onpay.models.Operation.objects.create(user=request.user,
                                            sum=form.cleaned_data['sum']).id

        iframe = iframe_generator.iframe_tag(op_id, form.cleaned_data['sum'],
                                            email=request.user.email)

        if request.is_ajax():
            return HttpResponse(iframe)

        return direct_to_template(request, iframe_template_name, extra_context={
            "iframe": iframe,
            "referer": request.META['HTTP_REFERER'],
            })

    return direct_to_template(request, template_name, extra_context={"form": form})


def onpay_pay(request):
    if get_constant("debug"):
        mail_admins(subject=u"Pay query", message=unicode(dict(request.POST)))
    form = onpay.forms.OnpayPayForm(request.POST)
    if not form.is_valid():
        return HttpResponse(answerpay_dict(request.POST, 12,
            u'Error in parameters data: %s' % form.errors))

    try:
        onpay.models.data_get_created_operation(form.cleaned_data['pay_for'])
    except onpay.models.Operation.DoesNotExist:
        return HttpResponse(answerpay_dict(request.POST, 10,
        'Cannot find any pay rows acording to this parameters: wrong payment'))

    if not form.check_md5():
        return HttpResponse(answerpay_dict(request.POST, 8,
            'Md5 signature is wrong.'))
    else:
        rezult_balance = onpay.models.data_update_user_balance(
            form.cleaned_data['pay_for'], form.cleaned_data['order_amount']
            ) if get_constant('use_balance_table', True) else True
        # устанавливаем статус операции как оплаченную
        rezult_operation = onpay.models.Operation.objects.filter(
                id=form.cleaned_data['pay_for']).update(status=1)
        # если оба запроса прошли успешно выдаем ответ об удаче,
        # если нет, то о том что операция не произошла
        if rezult_operation and rezult_balance:
            return HttpResponse(answerpay_dict(request.POST, 0, 'OK'))
        else:
            print rezult_operation, rezult_balance
            return HttpResponse(answerpay_dict(request.POST, 9,
                'Error in mechant database queries: operation or balance '
                'tables error'))



@csrf_exempt
def process_api_request(request):
    if (request.REQUEST['type'] == 'check'):
        return HttpResponse(answer_dict(request.POST, 0, 'OK'))
    if (request.REQUEST['type'] == 'pay'):
        return onpay_pay(request)
    return HttpResponse('')
