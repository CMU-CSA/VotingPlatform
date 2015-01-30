from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User
from VotingPlatform.models import Round, Candidate, CandidatePair

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        self.stdout.write("-- Creating admin")
        admin = User.objects.create_user(username='cmucsa', first_name='Harry', last_name='zeng', password='santiwansui')
        admin.save()
        self.stdout.write("-- Initializing round")
        r = Round()
        r.save()
        
        self.stdout.write("-- initialization complete")