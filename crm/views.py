from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localdate
from .models import DailyStatistic
from .forms import DailyStatisticForm
from openpyxl import Workbook
from django.http import HttpResponse

@login_required
def daily_report(request):
    today = localdate()  # текущая дата (учитывая настройки таймзоны)
    report, created = DailyStatistic.objects.get_or_create(manager=request.user, report_date=today)
    if request.method == 'POST':
        form = DailyStatisticForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('daily_report')
    else:
        form = DailyStatisticForm(instance=report)
    return render(request, 'daily_report.html', {'form': form})

@login_required
def statistics(request):
    overall_stats = DailyStatistic.objects.all().order_by('-timestamp')
    my_stats = DailyStatistic.objects.filter(manager=request.user).order_by('-timestamp')

    my_totals = {
        'contacts_count': sum(stat.contacts_count for stat in my_stats),
        'organizations_count': sum(stat.organizations_count for stat in my_stats),
        'blocked_telegram_count': sum(stat.blocked_telegram_count for stat in my_stats),
    }
    overall_totals = {
        'contacts_count': sum(stat.contacts_count for stat in overall_stats),
        'organizations_count': sum(stat.organizations_count for stat in overall_stats),
        'blocked_telegram_count': sum(stat.blocked_telegram_count for stat in overall_stats),
    }
    context = {
        'overall_stats': overall_stats,
        'my_stats': my_stats,
        'my_totals': my_totals,
        'overall_totals': overall_totals,
    }
    return render(request, "statistics.html", context)

@staff_member_required
def export_excel(request):
    report_date = request.GET.get('report_date')
    manager_id = request.GET.get('manager_id')
    qs = DailyStatistic.objects.all().order_by('-report_date')
    if report_date:
        qs = qs.filter(report_date=report_date)
    if manager_id:
        qs = qs.filter(manager_id=manager_id)

    wb = Workbook()
    ws = wb.active
    ws.title = "Daily Statistics"

    headers = ["Менеджер", "Дата", "Контакты", "Организации", "Заблокированные Telegram"]
    ws.append(headers)

    for stat in qs:
        ws.append([
            stat.manager.username,
            stat.report_date.strftime("%Y-%m-%d"),
            stat.contacts_count,
            stat.organizations_count,
            stat.blocked_telegram_count,
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    filename = f"daily_statistics_{report_date or 'all'}.xlsx"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response

@staff_member_required
def admin_statistics(request):
    # Выбираем все записи, можно отсортировать по report_date, затем по менеджеру
    stats = DailyStatistic.objects.all().order_by('-report_date', 'manager')
    context = {
        'stats': stats,
    }
    return render(request, "admin_statistics.html", context)

@staff_member_required
def view_stat(request, stat_id):
    stat = DailyStatistic.objects.get(id=stat_id)
    return render(request, "view_stat.html", {"stat": stat})

