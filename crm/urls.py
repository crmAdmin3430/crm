from django.urls import path
from .views import daily_report, statistics, export_excel, admin_statistics, view_stat

urlpatterns = [
    path('daily-report/', daily_report, name='daily_report'),
    path('statistics/', statistics, name='statistics'),
    path('admin-statistics/', admin_statistics, name='admin_statistics'),
    path('view-stat/<int:stat_id>/', view_stat, name='view_stat'),
    path('export-excel/', export_excel, name='export_excel'),

]