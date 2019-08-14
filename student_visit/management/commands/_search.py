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


class Command(BaseCommand):
    help = 'Search for  StudentVisitModel objects'

    def add_arguments(self, parser):
        """
        Add arguments to the command.
        """
        parser.add_argument(
            '--no-detail',
            action='store_false',
            dest='show-detail',
            default=True,
            help=
            'By default, when only one result is returned, details will be printed also.  Giving this flag supresses this behaviour',
        )
        parser.add_argument(
            'term',
            nargs="+",
            help='Search constraints',
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
        obj_list = Model.objects.search(options['term'])
        if options['show-detail'] and obj_list.count() == 1:
            obj = obj_list.get()
            s = object_detail(obj)
            sys.stdout.write(self.style.SUCCESS(s))
        else:
            for obj in obj_list:
                s = "{}".format(obj.pk) + '\t' + "{}".format(obj)
                sys.stdout.write(self.style.SUCCESS(s))


#######################################################################
