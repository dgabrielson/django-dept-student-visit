"""
Views for the student_visit application
"""
#######################
from __future__ import print_function, unicode_literals

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from formtools.wizard.views import SessionWizardView

from admin_export.views import ExportSpreadsheet

from . import conf
from .forms import AgreeForm, SectionForm, StudentNumberForm
from .models import Reason, StudentVisit

#######################
#######################################################################

#######################################################################


class ReasonMixin(object):
    queryset = Reason.objects.active()


#######################################################################


class ReasonListView(ReasonMixin, ListView):
    """
    List the reasons
    """


#######################################################################


class ReasonDetailView(ReasonMixin, DetailView):
    """
    Detail for the Reason
    """


#######################################################################


def student_agree_conditional(wizard):
    """
    Return True when the AgreeForm should be displayed; False otherwise.
    """
    cleaned_data = wizard.get_cleaned_data_for_step(step='0')
    if cleaned_data is None:
        return True
    stdnum = cleaned_data.get('student_number', None)
    reason = wizard._get_reason()
    qs = StudentVisit.objects.filter(
        active=True, reason=reason, student__student_number=stdnum, agree=True)
    return not qs.exists()


#######################################################################


@method_decorator(csrf_exempt, name='dispatch')
class StudentViewFormWizardView(SessionWizardView):
    """
    This view must have a ``reason_slug`` arg to specify the reason.
    """
    form_list = [
        StudentNumberForm,
        SectionForm,
        AgreeForm,
    ]
    template_name = 'student_visit/visit_wizard.html'

    def _get_reason(self):
        if not hasattr(self, '_reason'):
            self._reason = get_object_or_404(
                Reason, active=True, slug=self.kwargs.get('reason_slug', None))
        return self._reason

    def get_form_kwargs(self, step):
        # determine the step if not given
        form_kwargs = super(StudentViewFormWizardView,
                            self).get_form_kwargs(step)
        reason = self._get_reason()
        if step == '0':  # StudentNumberForm
            form_kwargs['reason'] = reason
        if step == '1':  # SectionForm
            from classes.models import Section
            section_qs = Section.objects.active()
            if reason.term:
                section_qs = section_qs.filter(term=reason.term)
            prev_data = self.storage.get_step_data('0')
            if prev_data is not None:
                stdnum = prev_data.get('0-student_number', None)
                section_qs = section_qs.filter(
                    registration_list__student__student_number=stdnum)
                form_kwargs['section_qs'] = section_qs
            else:
                # Error condition observed 2017-Oct-20
                form_kwargs['section_qs'] = section_qs.none()
        return form_kwargs

    def get_form_initial(self, step):
        initial = super(StudentViewFormWizardView, self).get_form_initial(step)
        if step == '2':
            initial['i_agree'] = not conf.get('visit-wizard:i_agree:required')
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super(StudentViewFormWizardView, self).get_context_data(
            *args, **kwargs)
        context['reason'] = self._get_reason()
        context['wizard_step'] = self.steps.current
        return context

    def get_done_url(self):
        url = conf.get('visit-wizard:get_redirect_url')
        if callable(url):
            url = url(self)
        return url

    def done(self, form_list, **kwargs):
        # construct the StudentVisit object and save.
        student_form, section_form = list(form_list)[:2]
        if student_agree_conditional(self):
            agree_form = list(form_list)[2]
            i_agree = agree_form.cleaned_data['i_agree']
        else:
            i_agree = True
        visit = StudentVisit.objects.create(
            student=student_form.student,
            reason=self._get_reason(),
            agree=i_agree)
        sections = section_form.cleaned_data['sections']
        visit.sections.set(sections)
        messages.success(
            self.request,
            _('Thanks! Your visit has been recorded.'),
            fail_silently=True)
        return HttpResponseRedirect(self.get_done_url())


#######################################################################
#######################################################################

class AdminExportVisitsCSV(ExportSpreadsheet):

    def get_contenttype(self):
        """
        Get the content type of the model.
        """
        ct = ContentType.objects.get_for_model(StudentVisit)
        return ct

    def get_queryset(self):
        reason_qs = Reason.objects.filter(pk=self.kwargs['pk'])
        visit_qs = StudentVisit.objects.filter(
                    reason__in=reason_qs,
                    active=True).distinct()
        qs = self.security_filter(visit_qs)
        return qs

    def get_format(self):
        """
        Get the format for the spreadsheet.
        """
        return 'csv'

#######################################################################
