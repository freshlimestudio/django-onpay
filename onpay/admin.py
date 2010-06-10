# -*- coding: utf-8 -*-
#~ from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

import onpay.models

class OperationAdmin(admin.ModelAdmin):
    raw_id_fields = "user",
    list_display = "date", "id", "user", "sum", "status"
    list_filter = "status",

class BalanceAdmin(admin.ModelAdmin):
    raw_id_fields = "user",
    list_display = "date", "user", "sum"

admin.site.register(onpay.models.Operation, OperationAdmin)
admin.site.register(onpay.models.Balance, BalanceAdmin)
