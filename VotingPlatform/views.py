from django.shortcuts import render, redirect
from VotingPlatform.models import Candidate
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

def home(request):
    try:
        User.objects.get(username='admin')
    except ObjectDoesNotExist:
        admin = User.objects.create_user(username='admin', first_name='Harry', last_name='zeng', password='admin')
        admin.save()
    return render(request, 'index.html')

def user_login(request):
    if not 'name' in request.POST or not request.POST['name'] \
        or not 'password' in request.POST or not request.POST['password']:
        return render(request, 'error.html')
    username = request.POST['name']
    password = request.POST['password']
    user_auth = authenticate(username=username, password=password)
    if not user_auth:
        return render(request, 'error.html')
    login(request, user_auth)
    return redirect('/manage/')

def voting_page(request):
    candidates = Candidate.objects.all()
    return render(request, 'voting.html', {"candidates":candidates})

@login_required
def admin_page(request):
    candidates = Candidate.objects.all()
    return render(request, 'admin.html', {"candidates":candidates})

@login_required
def add_candidate(request):
    if not 'name' in request.POST or not request.POST['name'] \
        or not 'information' in request.POST or not request.POST['information']:
        return render(request, 'error.html')
    name = request.POST['name']
    information = request.POST['information']
    try:
        Candidate.objects.get(name = name)
        return render(request, 'error.html')
    except ObjectDoesNotExist:
        candidate = Candidate.objects.create(name = name, information = information)
        candidate.save()
        return redirect('/manage/')
    
@login_required
def remove_candidate(request):
    if not 'name' in request.POST or not request.POST['name']:
        return render(request, 'error.html')
    name = request.POST['name']
    try:
        candidate = Candidate.objects.get(name = name)
        candidate.delete()
        return redirect('/manage/')
    except ObjectDoesNotExist:
        return render(request, 'error.html')

@transaction.atomic
def vote(request):
    if not 'name' in request.POST or not request.POST['name']:
        return render(request, 'error.html')
    try:
        candidate = Candidate.objects.get(name = request.POST['name'])
    except ObjectDoesNotExist:
        return render(request, 'error.html')
    candidate.vote()
    return redirect('/voting/')