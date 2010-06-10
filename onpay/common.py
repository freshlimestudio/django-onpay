# coding: UTF-8
import urllib
from hashlib import md5
from lxml import etree

from onpay.conf import get_constant

class IframeGenerator(object):
    def __init__(self):
        self.pay_mode = get_constant("pay_mode", "fix")
        self.currency = get_constant("currency", "RUR")
        self.convert  = get_constant("convert", "yes")
        self.url_success = get_constant("url_success")
        self.private_code = get_constant("private_code")
        self.onpay_login = get_constant("onpay_login")
        self.set_f(get_constant("f"))

    def iframe_url_params(self, operation_id, summ, email=None):
        "Функция определения параметров платежной формы."
        query = {
            "pay_mode": self.pay_mode,
            "currency": self.currency,
            "convert":  self.convert,

            "pay_for": operation_id,
            "price": summ,
            "md5": self.md5check(summ, operation_id),
        }
        if self.url_success:
            query["url_success"] = self.url_success
        if email:
            query['user_email'] = email
        if self.f:
            query['f'] = self.f
        return urllib.urlencode(query)

    def md5check (self, summ, operation_id):
        return md5(";".join(
            (self.pay_mode, str(summ), self.currency, str(operation_id),
            self.convert, self.private_code,))).hexdigest().upper()

    def set_f(self, f):
        "Определение ширины и высоты в зависимости от текущего скина"
        self.f = f
        self.width, self.height = {
            None: ( 300, 500),
            1:    (1020, 660),
            2:    ( 250, 540),
            3:    ( 960, 800),
        }[f]

    def iframe_tag (self, operation_id, summ, email=None):
        url = "http://secure.onpay.ru/pay/%s?%s" % (self.onpay_login,
            self.iframe_url_params(operation_id, summ, email=email))
        options = {
            "src": url,
            "width": self.width,
            "height": self.height,
            "frameborder": "no",
            "scrolling": "no",
            "name": "onpay",
            "id": "onpay",
        }
        options_gen = ((u'%s="%s"' % o_0) for o_0 in options.iteritems())
        return u'<iframe %s></iframe>' % (u" ".join(options_gen))

def answer(type, code, pay_for, order_amount, order_currency, text):
    "функция выдает ответ для сервиса onpay в формате XML на чек запрос"
    array_for_md5 = (type, pay_for, order_amount, order_currency, str(code),
                     get_constant('private_code'))
    result_md5 = md5(";".join(array_for_md5)).hexdigest().upper()

    root = etree.Element("result")
    etree.SubElement(root, "code").text = str(code)
    etree.SubElement(root, "pay_for").text = pay_for
    etree.SubElement(root, "comment").text = text
    etree.SubElement(root, "md5").text = result_md5
    return etree.tostring(root, pretty_print=True,
                            xml_declaration=True, encoding='UTF-8')


def answer_dict(POST, code, text):
    "Shortcut for call answer with POST or form dict as parameter"
    return answer(
        POST.get("type"),
        code,
        POST.get("pay_for"),
        POST.get("order_amount"),
        POST.get("order_currency"),
        text,
    )

def answerpay(type, code, pay_for, order_amount, order_currency, text, onpay_id):
    "функция выдает ответ для сервиса onpay в формате XML на pay запрос"

    array_for_md5 = (type, pay_for, onpay_id, pay_for, order_amount,
                    order_currency, str(code), get_constant('private_code'))
    result_md5 = md5(";".join(array_for_md5)).hexdigest().upper()

    root = etree.Element("result")
    etree.SubElement(root, "code").text = str(code)
    etree.SubElement(root, "comment").text = text
    etree.SubElement(root, "onpay_id").text = onpay_id
    etree.SubElement(root, "pay_for").text = pay_for
    etree.SubElement(root, "order_id").text = pay_for
    etree.SubElement(root, "md5").text = result_md5
    return etree.tostring(root, pretty_print=True,
                            xml_declaration=True, encoding='UTF-8')

def answerpay_dict(request_dict, code, text):
    "Shortcut for call answerpay with POST or form dict as parameter"
    return answerpay(
        request_dict.get('type'),
        code,
        request_dict.get('pay_for'),
        request_dict.get('order_amount'),
        request_dict.get('order_currency'),
        unicode(text),
        request_dict.get('onpay_id'),
    )
