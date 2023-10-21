from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Department, Feedback, FeedbackItem

admin.site.register(User, UserAdmin)
admin.site.register(Department, admin.ModelAdmin)
admin.site.register(Feedback, admin.ModelAdmin)
admin.site.register(FeedbackItem, admin.ModelAdmin)
