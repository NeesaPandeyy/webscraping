from django.contrib import admin
from django_celery_beat.models import (ClockedSchedule, CrontabSchedule,
                                       IntervalSchedule, PeriodicTask,
                                       SolarSchedule)
from unfold.admin import ModelAdmin

admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(ModelAdmin):
    list_display = ["name", "interval", "crontab", "enabled", "last_run_at"]
    search_fields = ["name", "task"]
    list_filter = ["enabled", "start_time", "last_run_at"]


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(ModelAdmin):
    list_display = ["every", "period"]


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(ModelAdmin):
    list_display = ["minute", "hour", "day_of_week", "day_of_month", "month_of_year"]


@admin.register(SolarSchedule)
class SolarScheduleAdmin(ModelAdmin):
    list_display = ["event", "latitude", "longitude"]


@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(ModelAdmin):
    list_display = ["clocked_time"]
