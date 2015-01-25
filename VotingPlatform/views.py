from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from mimetypes import guess_type
from VotingPlatform.models import Candidate, CandidatePair
from VotingPlatform.forms import CandidateForm
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
    return redirect(reverse('manage'))

def voting_page(request):
    pairs = CandidatePair.objects.all()
    return render(request, 'voting.html', {"pairs":pairs})

@login_required
def admin_page(request):
    candidates = Candidate.objects.all()
    pairs = CandidatePair.objects.all()
    context = {'form':CandidateForm(), 'candidates':candidates, 'pairs':pairs}
    return render(request, 'admin.html', context)

@login_required
@transaction.atomic
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
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if not form.is_valid():
            context = {'form':form}
            return render(request, 'simple-address-book/add-entry.html', context)
        form.save()
        return redirect(reverse('manage'))
    
@login_required
@transaction.atomic
def remove_candidate(request):
    if not 'name' in request.POST or not request.POST['name']:
        return render(request, 'error.html')
    name = request.POST['name']
    try:
        candidate = Candidate.objects.get(name = name)
        candidate.picture.delete()
        candidate.delete()
        return redirect(reverse('manage'))
    except ObjectDoesNotExist:
        return render(request, 'error.html')

@login_required
@transaction.atomic
def pair_candidates(request):
    if not 'name1' in request.POST or not request.POST['name1'] \
        or not 'name2' in request.POST or not request.POST['name2']:
        return render(request, 'error.html')
    name1 = request.POST['name1']
    name2 = request.POST['name2']
    try:
        candidate1 = Candidate.objects.get(name = name1)
        candidate2 = Candidate.objects.get(name = name2)
        pair = CandidatePair(first = candidate1, second = candidate2)
        pair.save()
        return redirect(reverse('manage'))
    except ObjectDoesNotExist:
        return render(request, 'error.html')

@login_required
@transaction.atomic
def unpair_candidates(request):
    if not 'pid' in request.POST or not request.POST['pid']:
        return render(request, 'error.html')
    pid = request.POST['pid']
    try:
        pair = CandidatePair.objects.get(id = pid)
        pair.delete()
        return redirect(reverse('manage'))
    except ObjectDoesNotExist:
        return render(request, 'error.html')

def get_photo(request, cid):
    entry = get_object_or_404(Candidate, id=cid)
    if not entry.picture:
        raise Http404
    content_type = guess_type(entry.picture.name)
    return HttpResponse(entry.picture, content_type=content_type)

@transaction.atomic
def vote(request):
    if not 'name' in request.POST or not request.POST['name']:
        return render(request, 'error.html')
    try:
        candidate = Candidate.objects.get(name = request.POST['name'])
    except ObjectDoesNotExist:
        return render(request, 'error.html')
    candidate.vote()
    return render(request, 'success.html')