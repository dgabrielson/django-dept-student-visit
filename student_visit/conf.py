"""
The DEFAULT configuration is loaded when the named _CONFIG dictionary
is not present in your settings.
"""
#######################
from __future__ import print_function, unicode_literals

from django.conf import settings
from django.urls import reverse_lazy

#######################

CONFIG_NAME = 'STUDENT_VISIT_CONFIG'  # must be uppercase!


def _default_visit_wizard_redirect_url(wizard_view):
    return reverse_lazy(
        'studentvisit-reason-detail',
        kwargs={'slug': wizard_view.kwargs['reason_slug']})


DEFAULT = {

    # either a string or a callable with the signature f(view) -> url
    'visit-wizard:get_redirect_url': _default_visit_wizard_redirect_url,

    # Is agreement required to continue?
    'visit-wizard:i_agree:required': False,
}

#########################################################################


def get(setting):
    """
    get(setting) -> value

    setting should be a string representing the application settings to
    retrieve.
    """
    assert setting in DEFAULT, 'the setting %r has no default value' % setting
    app_settings = getattr(settings, CONFIG_NAME, DEFAULT)
    return app_settings.get(setting, DEFAULT[setting])


def get_all():
    """
    Return all current settings as a dictionary.
    """
    app_settings = getattr(settings, CONFIG_NAME, DEFAULT)
    return dict([(setting, app_settings.get(setting, DEFAULT[setting])) \
                 for setting in DEFAULT])


#########################################################################
