from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Department, Feedback, FeedbackItem

admin.site.register(Department, admin.ModelAdmin)
admin.site.register(Feedback, admin.ModelAdmin)
admin.site.register(FeedbackItem, admin.ModelAdmin)


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Рабочие данные', {'fields': (
            'department',
            'position',
            'is_intern',
            'is_head',
        )}),
        ('Отзывы', {'fields': (
            'is_awaiting_feedback',
            'feedback_viewed'
        )})
    )


admin.site.register(User, CustomUserAdmin)
