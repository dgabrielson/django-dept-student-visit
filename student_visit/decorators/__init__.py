"""
Reusable library of decorators.
"""
#######################
from __future__ import unicode_literals, print_function
#######################

from .admin_extras import admin_link, admin_changelist_link

__all__ = [
    'admin_link',
    'admin_changelist_link',
]
