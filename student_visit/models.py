"""
Models for the student_visit application.
"""
from __future__ import print_function, unicode_literals

from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible

from .querysets import ReasonQuerySet, StudentVisitQuerySet

#######################################################################
#######################################################################
#######################################################################


class StudentVisitBaseModel(models.Model):
    """
    An abstract base class.
    """
    active = models.BooleanField(default=True)
    created = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name='creation time')
    modified = models.DateTimeField(
        auto_now=True, editable=False, verbose_name='last modification time')

    class Meta:
        abstract = True


#######################################################################
#######################################################################
#######################################################################


@python_2_unicode_compatible
class Reason(StudentVisitBaseModel):
    """
    A description of this model.
    """
    slug = AutoSlugField(
        max_length=64, unique=True, populate_from='verbose_name')
    verbose_name = models.CharField(max_length=64)
    ordering = models.PositiveSmallIntegerField(default=100)
    term = models.ForeignKey(
        'classes.Semester', null=True, blank=True, on_delete=models.SET_NULL)

    objects = ReasonQuerySet.as_manager()

    class Meta:
        ordering = ('ordering', '-term', 'verbose_name')

    def __str__(self):
        return self.verbose_name

    def get_absolute_url(self):
        return reverse(
            'studentvisit-reason-detail', kwargs={'slug': self.slug})


#######################################################################
#######################################################################
#######################################################################


@python_2_unicode_compatible
class StudentVisit(StudentVisitBaseModel):
    """
    A description of this model.
    """
    reason = models.ForeignKey(
        Reason, limit_choices_to={'active': True}, on_delete=models.PROTECT)
    student = models.ForeignKey(
        'students.Student',
        limit_choices_to={'active': True},
        on_delete=models.CASCADE)
    when = models.DateTimeField(auto_now_add=True)
    agree = models.BooleanField(default=False)
    sections = models.ManyToManyField(
        'classes.Section', limit_choices_to={'active': True}, blank=True)

    objects = StudentVisitQuerySet.as_manager()

    class Meta:
        ordering = ('-when', )

    def __str__(self):
        return '{} - {} - {}'.format(self.reason, self.student, self.when)


#     def get_absolute_url(self):
#         return reverse('studentvisit-visit-detail', kwargs={'pk': self.pk})

#######################################################################
#######################################################################
#######################################################################
