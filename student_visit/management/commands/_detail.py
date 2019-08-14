#######################################################################
#######################
from __future__ import print_function, unicode_literals

from django.core.management.base import BaseCommand, CommandError

from ...models import StudentVisitModel as Model
from ._utils import object_detail

#######################
## https://docs.djangoproject.com/en/dev/howto/custom-management-commands/
################################################################

#######################################################################

#######################################################################

M2M_FIELDS = []
RELATED_ONLY = None  # Specify a list or None; None means introspect for related
RELATED_EXCLUDE = []  # any related fields to skip

#######################################################################


class Command(BaseCommand):
    help = 'Get detail on an StudentVisitModel object, including related objects'

    def add_arguments(self, parser):
        """
        Add arguments to the command.
        """
        parser.add_argument(
            '-r',
            '--related',
            nargs='*',
            help='Specify related fields to include (introspected by default)',
        )
        parser.add_argument(
            '-x',
            '--exclude',
            nargs='*',
            help='Specify related fields to exclude',
        )
        parser.add_argument(
            'pk',
            nargs='+',
            type=int,
            help='Primary key(s) of objects to display',
        )

# When you are using management commands and wish to provide console output,
# you should write to self.stdout and self.stderr, instead of printing to
# stdout and stderr directly. By using these proxies, it becomes much easier
# to test your custom command. Note also that you don't need to end messages
# with a newline character, it will be added automatically, unless you
# specify the ``ending`` parameter to write()

    def handle(self, *args, **options):
        """
        Do the thing!
        """
        related = options.get('related', RELATED_ONLY)
        exclude = options.get('exclude', RELATED_EXCLUDE)
        for pk in options['pk']:
            obj = Model.objects.get(pk=pk)
            s = object_detail(obj, M2M_FIELDS, related, exclude)
            sys.stdout.write(self.style.SUCCESS(s))


#######################################################################
