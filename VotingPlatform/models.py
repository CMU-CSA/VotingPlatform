from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length = 64)
    votes_first_round = models.IntegerField(default = 0)
    votes_second_round = models.IntegerField(default = 0)
    votes_judge = models.IntegerField(default = 0)
    information = models.CharField(max_length = 8192)
    picture = models.ImageField(upload_to = 'pictures', blank=True)
    round = models.IntegerField(default = 1)
    
    def vote_first_round(self):
        self.votes_first_round = self.votes_first_round + 1
        self.save()

"""
class CandidatePair(models.Model):
    first = models.ForeignKey(Candidate, related_name = "first")
    second = models.ForeignKey(Candidate, related_name = "second")

    def set_winner(self):
        winner = self.first if self.first.votes_first_round > self.second.votes_first_round else self.second
        winner.round = winner.round + 1
        winner.save()
"""

class Session(models.Model):
    sessionid = models.CharField(max_length = 128)
    first_voted = models.BooleanField(default = False)
    second_voted = models.BooleanField(default = False)
    
class Round(models.Model):
    round = models.IntegerField(default = 1)
    open = models.BooleanField(default = False)
    
    def toggle_voting(self, enable):
        self.open = enable
        self.save()
        
class TicketNumber(models.Model):
    number = models.IntegerField()
    first_voted = models.BooleanField(default = False)
    second_voted = models.BooleanField(default = False)

class AndrewIDs(models.Model):
    andrewId = models.CharField(max_length = 20)
    first_voted = models.BooleanField(default = False)
    second_voted = models.BooleanField(default = False)
    is_judge = models.BooleanField(default = False)