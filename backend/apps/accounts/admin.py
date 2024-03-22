from django.contrib import admin
from .models import CustomUser, Partner, RegularUser


admin.site.register(CustomUser)
admin.site.register(RegularUser)
admin.site.register(Partner)

