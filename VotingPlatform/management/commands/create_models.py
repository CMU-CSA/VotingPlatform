from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User
from VotingPlatform.models import Round, Candidate, CandidatePair

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        self.stdout.write("-- Creating admin")
        admin = User.objects.create_user(username='admin', first_name='Harry', last_name='zeng', password='admin')
        admin.save()
        self.stdout.write("-- Initializing round")
        r = Round()
        r.save()
        
        self.stdout.write("-- Initializing sample candidates")
        a1 = Candidate(name = "A1", information = "sample")
        a2 = Candidate(name = "A2", information = "sample")
        b1 = Candidate(name = "B1", information = "sample")
        b2 = Candidate(name = "B2", information = "sample")
        c1 = Candidate(name = "C1", information = "sample")
        c2 = Candidate(name = "C2", information = "sample")
        d1 = Candidate(name = "D1", information = "sample")
        d2 = Candidate(name = "D2", information = "sample")
        e1 = Candidate(name = "E1", information = "sample")
        e2 = Candidate(name = "E2", information = "sample")
        f1 = Candidate(name = "F1", information = "sample")
        f2 = Candidate(name = "F2", information = "sample")
        
        a1.save()
        a2.save()
        b1.save()
        b2.save()
        c1.save()
        c2.save()
        d1.save()
        d2.save()
        e1.save()
        e2.save()
        f1.save()
        f2.save()
        
        self.stdout.write("-- Initializing sample pairs")
        pa = CandidatePair(first = a1, second = a2)
        pb = CandidatePair(first = b1, second = b2)
        pc = CandidatePair(first = c1, second = c2)
        pd = CandidatePair(first = d1, second = d2)
        pe = CandidatePair(first = e1, second = e2)
        pf = CandidatePair(first = f1, second = f2)
        
        pa.save()
        pb.save()
        pc.save()
        pd.save()
        pe.save()
        pf.save()
        
        self.stdout.write("-- initialization complete")