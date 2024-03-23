from django.contrib import admin
from .models import CustomUser, Partner, RegularUser, ChatMessage


admin.site.register(CustomUser)
admin.site.register(RegularUser)
admin.site.register(ChatMessage)
admin.site.register(Partner)


