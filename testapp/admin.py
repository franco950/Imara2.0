from django.contrib import admin

from .models import transaction,alert,report,blacklist,CustomUser,systemsettings
admin.site.register(alert)
admin.site.register(report)
admin.site.register(transaction)
admin.site.register(blacklist)
admin.site.register(CustomUser)
admin.site.register(systemsettings)