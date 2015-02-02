from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User
from VotingPlatform.models import TicketNumber

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        for i in range(1, 400):
            t = TicketNumber(number = i)
            t.save()