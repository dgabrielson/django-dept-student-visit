#######################################################################
#######################
from __future__ import print_function, unicode_literals

from django.core.management.base import BaseCommand, CommandError

from ...models import StudentVisitModel as Model
from ._utils import resolve_fields

#######################
## https://docs.djangoproject.com/en/dev/howto/custom-management-commands/
################################################################

#######################################################################

#######################################################################


class Command(BaseCommand):
    help = 'List of StudentVisitModel objects'

    def add_arguments(self, parser):
        """
        Add arguments to the command.
        """
        parser.add_argument(
            '-f',
            '--fields',
            dest='field_list',
            help=
            'Specify a comma delimited list of fields to include, e.g., -f "course.label,section_name,sectionschedule_set.all.0.instructor"',
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
        qs = Model.objects.active()
        for item in qs:
            value_list = map(lambda s: '{}'.format(s), [
                item.pk,
                item,
            ])
            if options['field_list']:
                value_list += resolve_fields(item,
                                             options['field_list'].split(','))
            s = '\t'.join(value_list)
            sys.stdout.write(self.style.SUCCESS(s))


#######################################################################
