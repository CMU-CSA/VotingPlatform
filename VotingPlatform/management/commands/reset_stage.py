from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User
from VotingPlatform.models import AndrewIDs, Candidate, Session
from django.core.exceptions import ObjectDoesNotExist

class Command(NoArgsCommand):

     def handle_noargs(self, **options):
        Session.objects.all().delete()
        self.stdout.write('-- All sessions deleted')
        for ticket in AndrewIDs.objects.all():
            ticket.first_voted = False
            ticket.second_voted = False
            ticket.save()
        self.stdout.write('-- All andrew ID reset')
        candidates = Candidate.objects.all()
        for candidate in candidates:
            candidate.votes_judge = 0
            candidate.votes_second_round = 0
            candidate.votes_first_round = 0
            candidate.save()
        self.stdout.write('-- All votes reset')
