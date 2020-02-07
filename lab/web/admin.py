from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from web import models as wm


@admin.register(wm.Course)
class CouseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'deleted']
    ordering = ['deleted', 'code']


@admin.register(wm.Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'course_name', 'professor_list', 'deleted']
    ordering = ['deleted', 'course__code']

    def course_name(self, obj):
        """"Show related Course with a link"""
        link = reverse('admin:web_course_change', args=[obj.course.id])
        return format_html(f'Curso <a href="{link}">{obj.course.name}</a>')

    def professor_list(self, obj):
        s = str()
        for p in obj.get_professors:
            s += f'{p}<br>'
        return format_html(s)


@admin.register(wm.Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['year', 'kind', 'date_start', 'date_end', 'assigment_start', 'assigment_end']
    ordering = ['-year', '-kind']


@admin.register(wm.LabSchedule)
class LabScheduleAdmin(admin.ModelAdmin):
    list_display = ['time_start', 'time_end', 'weekdays_list', 'capacity']

    DAYS = {
        128: 'MON',
        64: 'TUE',
        32: 'WED',
        16: 'THU',
        8: 'FRI',
        4: 'SAT',
        2: 'SUN'
    }
