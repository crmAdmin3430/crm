from django import forms
from .models import DailyStatistic

class DailyStatisticForm(forms.ModelForm):
    class Meta:
        model = DailyStatistic
        fields = ['contacts_count', 'organizations_count', 'blocked_telegram_count']
        labels = {
            'contacts_count': 'Количество контактов',
            'organizations_count': 'Количество организаций',
            'blocked_telegram_count': 'Заблокированные Telegram',
        }