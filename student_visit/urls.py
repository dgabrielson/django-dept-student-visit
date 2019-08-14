"""
The url patterns for the student_visit application.
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.ReasonListView.as_view(),
        name='studentvisit-reason-list',
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        views.ReasonDetailView.as_view(),
        name='studentvisit-reason-detail',
    ),
    url(
        r'^(?P<reason_slug>[\w-]+)/visit-wizard/$',
        views.StudentViewFormWizardView.as_view(
            condition_dict={'2': views.student_agree_conditional}),
        name='studentvisit-visit-wizard',
    ),
]
