from django.contrib import admin

from .models import User, Department, Feedback, FeedbackItem, WaitForReview, Metric


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'department', 'position', 'is_intern', 'is_head', 'is_awaiting_feedback')
    list_filter = ('department', 'position', 'is_intern', 'is_head', 'is_awaiting_feedback')
    fieldsets = (
        (None, {'fields': (
        'email', 'password', 'name', 'surname', 'photo', 'department', 'position', 'is_intern', 'is_head',
        'is_awaiting_feedback', 'feedback_viewed')}),
    )


@admin.register(WaitForReview)
class WaitForReviewAdmin(admin.ModelAdmin):
    fields = ["to_user", "from_users", "created_at"]
    list_display = ["to_user"]
    readonly_fields = ["created_at"]


admin.site.register(Department, admin.ModelAdmin)
admin.site.register(Feedback, admin.ModelAdmin)
admin.site.register(FeedbackItem, admin.ModelAdmin)
admin.site.register(Metric, admin.ModelAdmin)
