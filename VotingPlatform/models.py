from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length = 64)
    votes = models.IntegerField()
    information = models.CharField()
    
    def vote(self):
        self.votes = self.votes + 1