from django.shortcuts import render
from VotingPlatform.models import *
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    return render(request, 'index.html')

def vote(request):
    if not 'candidate' in request.POST or not request.POST['candidate']:
        return render(request, 'error.html')
    try:
        candidate = Candidate.objects.get(name = request.POST['candidate'])
    except ObjectDoesNotExist:
        return render(request, 'error.html')
    candidate.vote()
    candidate.save()
    return render(request, 'success.html')