from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length = 64)
    votes = models.IntegerField(default = 0)
    information = models.CharField(max_length = 8192)
    picture = models.ImageField(upload_to = 'pictures', blank=True)
    
    def vote(self):
        self.votes = self.votes + 1
        self.save()