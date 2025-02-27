from django.contrib import admin
from .models import DailyStatistic


class DailyStatisticAdmin(admin.ModelAdmin):
    list_display = ('manager', 'report_date', 'contacts_count', 'organizations_count', 'blocked_telegram_count')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Суперпользователь (админ) видит все записи,
        # менеджеры – только свои записи.
        if request.user.is_superuser:
            return qs
        return qs.filter(manager=request.user)

    def save_model(self, request, obj, form, change):
        # Если не админ, принудительно ставим менеджера равным текущему пользователю
        if not request.user.is_superuser:
            obj.manager = request.user
        super().save_model(request, obj, form, change)


admin.site.register(DailyStatistic, DailyStatisticAdmin)