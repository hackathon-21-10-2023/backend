from django.contrib import admin

from .models import User, Department, Feedback, FeedbackItem


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'department', 'position', 'is_intern', 'is_head', 'is_awaiting_feedback')
    list_filter = ('department', 'position', 'is_intern', 'is_head', 'is_awaiting_feedback')
    fieldsets = (
        (None, {'fields': ('name', 'surname', 'email', 'department', 'position', 'is_intern', 'is_head', 'is_awaiting_feedback', 'feedback_viewed')}),
    )


admin.site.register(Department, admin.ModelAdmin)
admin.site.register(Feedback, admin.ModelAdmin)
admin.site.register(FeedbackItem, admin.ModelAdmin)
