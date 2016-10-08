from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from VotingPlatform.models import TicketNumber

class Command(BaseCommand):
    
    def handle(self, **options):
        for i in range(1, 400):
            t = TicketNumber(number = i)
            t.save()