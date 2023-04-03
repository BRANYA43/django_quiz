from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Send Today's Report to Admins"

    def handle(self, *args, **options):
        ...