from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localdate
from .models import DailyStatistic
from .forms import DailyStatisticForm
from openpyxl import Workbook
from django.http import HttpResponse


@login_required
def daily_report(request):
    if request.method == 'POST':
        form = DailyStatisticForm(request.POST)
        if form.is_valid():
            new_stat = form.save(commit=False)
            new_stat.manager = request.user
            # report_date можно оставить как есть или задать явно (например, timezone.localdate())
            new_stat.save()
            return redirect('daily_report')
    else:
        form = DailyStatisticForm()
    return render(request, 'daily_report.html', {'form': form})


@login_required
def statistics(request):
    today = localdate()
    # Только записи за текущий день
    my_stats = DailyStatistic.objects.filter(manager=request.user, report_date=today).order_by('-report_date')

    my_totals = {
        'contacts_count': sum(stat.contacts_count for stat in my_stats),
        'organizations_count': sum(stat.organizations_count for stat in my_stats),
        'blocked_telegram_count': sum(stat.blocked_telegram_count for stat in my_stats),
    }
    context = {
        'my_stats': my_stats,
        'my_totals': my_totals,
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

    headers = ["Менеджер", "Контакты", "Организации", "Заблокированные Telegram", "Дата создания"]
    ws.append(headers)

    for stat in qs:
        ws.append([
            stat.manager.username,
            stat.contacts_count,
            stat.organizations_count,
            stat.blocked_telegram_count,
            stat.created_at.strftime("%Y-%m-%d %H:%M"),
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
    # Группируем записи по report_date и суммируем поля
    aggregated_stats = DailyStatistic.objects.values('report_date').annotate(
        total_contacts=Sum('contacts_count'),
        total_orgs=Sum('organizations_count'),
        total_blocked=Sum('blocked_telegram_count')
    ).order_by('-report_date')

    context = {
        'aggregated_stats': aggregated_stats,
    }
    return render(request, "admin_statistics.html", context)
@staff_member_required
def view_stat(request, stat_id):
    stat = DailyStatistic.objects.get(id=stat_id)
    return render(request, "view_stat.html", {"stat": stat})

@staff_member_required
def view_stat_by_date(request):
    report_date = request.GET.get('report_date')
    if not report_date:
        return render(request, "view_stat_by_date.html", {"error": "Не указан report_date"})
    stats = DailyStatistic.objects.filter(report_date=report_date).order_by('manager__username')
    return render(request, "view_stat_by_date.html", {"stats": stats, "report_date": report_date})