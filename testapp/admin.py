from django.contrib import admin
from .models import transaction,alert,report,blacklist
admin.site.register(alert)
admin.site.register(report)
admin.site.register(transaction)
admin.site.register(blacklist)


