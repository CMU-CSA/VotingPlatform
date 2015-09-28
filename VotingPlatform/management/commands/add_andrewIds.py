from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User
from VotingPlatform.models import AndrewIDs
from django.core.exceptions import ObjectDoesNotExist

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        txt_file = open("VotingPlatform/andrewids.txt","r")
        andrew_ids = txt_file.readlines()
        for andrewid in andrew_ids:
            andrew_id = andrewid[0:-1]
            try:
                AndrewIDs.objects.get(andrewId = str(andrew_id))
                self.stdout.write('-- andrew ID: ' + str(andrew_id) + ' already exists')
            except ObjectDoesNotExist:
                aid = AndrewIDs(andrewId = str(andrew_id))
                aid.save()
                self.stdout.write('-- Audience andrew ID: ' + str(andrew_id) + ' added')
        self.stdout.write('-- andrew IDs scan complete')
