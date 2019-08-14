"""
Admin classes for the  student_visit application
"""
#######################

from __future__ import print_function, unicode_literals

from django.conf.urls import url
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

import admin_export

from .models import Reason, StudentVisit
from .views import AdminExportVisitsCSV

#######################################################################


@admin.register(Reason)
class ReasonAdmin(admin.ModelAdmin):

    list_display = ['verbose_name', 'term', 'changelist_buttons']

    def changelist_buttons(self, obj):
        if obj.pk:
            return format_html(
                '<a class="button" href="{}">CSV</a>&nbsp;',
                reverse(
                    'admin:student_visit_reason_export_spreadsheet_csv',
                    kwargs={
                        'pk': obj.pk,
                    }),
            )
        return ''

    changelist_buttons.short_description = 'Export'
    changelist_buttons.allow_tags = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        if admin_export is None:
            del actions['spreadsheet_export_action']
            del actions['csv_export_action']
        else:
            # remove the admin_export default export actions:
            if 'export_redirect_spreadsheet_xlsx' in actions:
                del actions['export_redirect_spreadsheet_xlsx']
            if 'export_redirect_spreadsheet_csv' in actions:
                del actions['export_redirect_spreadsheet_csv']
        return actions

    def get_urls(self):
        """
        Extend the admin urls for this model.
        Provide a link by subclassing the admin change_form,
        and adding to the object-tools block.
        """
        urls = super().get_urls()
        urls = [
            url(
                r'^(?P<pk>.+)/export/csv/$',
                self.admin_site.admin_view(AdminExportVisitsCSV.as_view()),
                name='student_visit_reason_export_spreadsheet_csv',
            ),
        ] + urls
        return urls



#######################################################################


@admin.register(StudentVisit)
class StudentVisitAdmin(admin.ModelAdmin):
    list_display = [
        'when',
        'student',
        'reason',
        'agree',
    ]
    list_filter = [
        'active',
        'when',
        'reason',
        'agree',
    ]
    readonly_fields = [
        'student',
        'reason',
        'sections',
        'when',
        'agree',
    ]
    search_fields = [
        'student__student_number',
        'student__person__cn',
    ]


#######################################################################
