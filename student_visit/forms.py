"""
Forms for the student_visit application.
"""
#######################
from __future__ import print_function, unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from classes.models import Section
from students.models import Student

from . import conf
from .models import Reason, StudentVisit

#######################
#######################################################################

#######################################################################


class StudentVisitForm(forms.ModelForm):
    """
    Form for the model.
    """

    class Meta:
        model = StudentVisit
        exclude = [
            'active',
        ]


#######################################################################
#######################################################################
#######################################################################


class StudentNumberForm(forms.Form):
    student_number = forms.CharField(max_length=16)

    class Media:
        css = {
            'all': (
                "css/forms.css",
                "student-visit/css/formwizard.css",
            )
        }

    def __init__(self, reason, *args, **kwargs):
        result = super(StudentNumberForm, self).__init__(*args, **kwargs)
        self.reason = reason
        return result

    def clean_student_number(self):
        # validate student number...
        student_qs = Student.objects.filter(active=True)
        if self.reason.term:
            student_qs = student_qs.filter(
                student_registration__section__term=self.reason.term)

        # Right now, the underlying model field is an IntegerField; however that may change...
        st_num = self.cleaned_data['student_number']
        try:
            st_num = int(st_num)
        except ValueError:
            raise forms.ValidationError(
                _("Please enter your student number (digits only)"))
        if st_num < 0:
            raise forms.ValidationError(
                _("Negative student numbers do not exist"))

        student_qs = student_qs.filter(student_number=st_num)
        if not student_qs.exists():
            raise forms.ValidationError(
                _("There was a problem with your student number"))
        self.student = student_qs.distinct().get()
        return st_num


#######################################################################


class SectionForm(forms.Form):
    sections = forms.ModelMultipleChoiceField(
        Section.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False)

    class Media:
        css = {
            'all': (
                "css/forms.css",
                "student-visit/css/formwizard.css",
            )
        }

    def __init__(self, section_qs, *args, **kwargs):
        result = super(SectionForm, self).__init__(*args, **kwargs)
        self.fields['sections'].queryset = section_qs
        return result

    def clean(self, *args, **kwargs):
        sections = self.cleaned_data.get('sections', None)
        if sections is None or not sections.exists():
            raise forms.ValidationError(
                "Please choose the course that you want help with.  You may choose more than one."
            )
        return super(SectionForm, self).clean(*args, **kwargs)


#######################################################################


class AgreeForm(forms.Form):
    i_agree = forms.BooleanField(
        required=conf.get('visit-wizard:i_agree:required'))

    class Media:
        css = {
            'all': (
                "css/forms.css",
                "student-visit/css/formwizard.css",
            )
        }


#######################################################################
