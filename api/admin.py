from django.contrib import admin
from .models import *


# Register your models here.

# admin.site.register(Wallet)
admin.site.register(Review)
# admin.site.register(Coffee)
#admin.site.register(PhoneOTP)
admin.site.register(Addmoney)
admin.site.register(Profile)
admin.site.register(Callm)
admin.site.register(CallResultm)



#dashboard
admin.site.register(ChargingStations)