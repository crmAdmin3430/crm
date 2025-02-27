# crm/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DailyStatistic(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    report_date = models.DateField(default=timezone.localdate)  # дата отчёта
    contacts_count = models.PositiveIntegerField(default=0)
    organizations_count = models.PositiveIntegerField(default=0)
    blocked_telegram_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('manager', 'report_date')
        ordering = ('-report_date',)

    def __str__(self):
        return f"{self.manager.username} – {self.report_date}"