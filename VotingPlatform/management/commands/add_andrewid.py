from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from VotingPlatform.models import AndrewIDs
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('judge_id', nargs='+', type = str)

    def handle(self, *args, **options):
        for andrew_id in options['judge_id']:
            try:
                AndrewIDs.objects.get(andrewId = andrew_id)
                self.stdout.write('-- Audience ID: ' + andrew_id + ' already exists')
            except ObjectDoesNotExist:
                audience = AndrewIDs(andrewId = andrew_id)
                audience.save()
                self.stdout.write('-- Audience ID: ' + andrew_id + ' added')
        self.stdout.write('Judge ID scan complete')
