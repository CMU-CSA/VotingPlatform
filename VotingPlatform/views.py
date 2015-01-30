from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from mimetypes import guess_type
from VotingPlatform.models import Candidate, CandidatePair, Round, Session
from VotingPlatform.forms import CandidateForm, CandidateEditForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

def current_round():
    return Round.objects.get(id = 1)

def error(request, reason, redirect_url = None, redirect = True):
    return render(request, "error.html", {'reason':reason, 'url':reverse('home') if not redirect_url else redirect_url, 'redirect': redirect})

def home(request):
    if request.user.is_authenticated():
        return redirect(reverse('manage'))
    else:
        return redirect(reverse('round' + str(current_round().round)))
    
def login_index(request):
    return render(request, 'index.html')

def user_login(request):
    if not 'name' in request.POST or not request.POST['name'] \
        or not 'password' in request.POST or not request.POST['password']:
        return error(request, 'Missing argument "name" or "password"')
    username = request.POST['name']
    password = request.POST['password']
    user_auth = authenticate(username=username, password=password)
    if not user_auth:
        return error(request, 'User authentication failed', reverse('index'))
    login(request, user_auth)
    return redirect(reverse('manage'))

@login_required
def user_logout(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect(reverse('home'))

def round1(request):
    rd = current_round()
    if not rd.open:
        return error(request, "Sorry. Voting will start soon!", redirect_url = reverse('round1'), redirect = False)
    if rd.round != 1:
        return redirect(reverse('round' + str(rd.round)))
    pairs = CandidatePair.objects.all()
    return render(request, 'round1.html', {'pairs':pairs})

def round2(request):
    rd = current_round()
    if not rd.open:
        return error(request, "Sorry. Voting will start soon!", redirect_url = reverse('round2'), redirect = False)
    if rd.round != 2:
        return redirect(reverse('round' + str(rd.round)))
    candidates = Candidate.objects.filter(round = 2)
    return render(request, 'round2.html', {'candidates':candidates})

@login_required
def admin_page(request):
    r = current_round()
    candidates = Candidate.objects.all()
    pairs = CandidatePair.objects.all()
    context = {'form':CandidateForm(), 'candidates':candidates, 'pairs':pairs, 'round':r}
    return render(request, 'admin.html', context)

@login_required
@transaction.atomic
def add_candidate(request):
    if not 'name' in request.POST or not request.POST['name'] \
        or not 'information' in request.POST or not request.POST['information']:
        return error(request, 'Missing argument "name" or "information"')
    name = request.POST['name']
    information = request.POST['information']
    try:
        Candidate.objects.get(name = name)
        return error(request, 'Candidate ' + name + ' already exists')
    except ObjectDoesNotExist:
        candidate = Candidate.objects.create(name = name, information = information)
        candidate.save()
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if not form.is_valid():
            return error(request, 'Form invalid')
        form.save()
        return redirect(reverse('manage'))
    
@login_required
@transaction.atomic
def remove_candidate(request):
    if not 'name' in request.POST or not request.POST['name']:
        return error(request, 'Missing argument "name" in request')
    name = request.POST['name']
    try:
        candidate = Candidate.objects.get(name = name)
        candidate.picture.delete()
        candidate.delete()
        return redirect(reverse('manage'))
    except ObjectDoesNotExist:
        return error(request, 'Candidate ' + name + ' does not exist')

@login_required
@transaction.atomic
def edit_candidate_page(request, cid):
    try:
        candidate = Candidate.objects.get(id = cid)
    except ObjectDoesNotExist:
        return error(request, 'Candidate #' + str(cid) + ' does not exist')
    return render(request, 'edit_candidate.html', {'form':CandidateEditForm(instance=candidate)})

@login_required
@transaction.atomic
def remove_picture(request):
    if not 'id' in request.POST or not request.POST['id']:
        return redirect(reverse('manage'))
    cid = request.POST['id']
    try:
        candidate = Candidate.objects.get(id = cid)
    except ObjectDoesNotExist:
        return redirect(reverse('manage'))
    candidate.picture.delete()
    return redirect(reverse('manage'))

@login_required
@transaction.atomic
def edit_candidate(request):
    if not 'id' in request.POST or not request.POST['id']:
        return error(request, 'Missing argument "id" in request')
    cid = request.POST['id']
    try:
        candidate = Candidate.objects.get(id = cid)
    except ObjectDoesNotExist:
        return error(request, 'Candidate #' + str(cid) + ' does not exist')
    form = CandidateEditForm(request.POST, request.FILES, instance=candidate)
    if not form.is_valid():
        return error(request, 'Form invalid')
    new_name = request.POST['name']
    try:
        c = Candidate.objects.get(name = new_name)
        if c.id != candidate.id: # name already exists
            return error(request, 'Candidate with name "' + new_name + '" already exists')
    except ObjectDoesNotExist:
        pass
    form.save()
    return redirect(reverse('manage'))

@login_required
@transaction.atomic
def pair_candidates(request):
    if not 'name1' in request.POST or not request.POST['name1'] \
        or not 'name2' in request.POST or not request.POST['name2']:
        return error(request, 'Missing argument "name1" or "name2" in request')
    name1 = request.POST['name1']
    name2 = request.POST['name2']
    try:
        candidate1 = Candidate.objects.get(name = name1)
        candidate2 = Candidate.objects.get(name = name2)
        pair = CandidatePair(first = candidate1, second = candidate2)
        pair.save()
        return redirect(reverse('manage'))
    except ObjectDoesNotExist:
        return error(request, 'Candidate ' + name1 + ' or ' + name2 + ' does not exist')

@login_required
@transaction.atomic
def unpair_candidates(request):
    if not 'pid' in request.POST or not request.POST['pid']:
        return error(request, 'Missing argument "pid" in request')
    pid = request.POST['pid']
    try:
        pair = CandidatePair.objects.get(id = pid)
        pair.delete()
        return redirect(reverse('manage'))
    except ObjectDoesNotExist:
        return error(request, "Candidate Pair #" + str(pid) + " does not exist")

@login_required
@transaction.atomic
def next_round(request):
    r = current_round()
    if r.round == 1:
        for pair in CandidatePair.objects.all():
            pair.set_winner()
        r.round = r.round + 1
        r.save()
    return redirect(reverse('manage'))

@login_required
@transaction.atomic
def prev_round(request):
    r = current_round()
    if r.round > 1:
        candidates = Candidate.objects.filter(round = r.round)
        for candidate in candidates:
            candidate.round = candidate.round - 1
            candidate.save()
        r.round = r.round - 1
        r.save()
    return redirect(reverse('manage'))

@login_required
@transaction.atomic
def enable_voting(request):
    current_round().toggle_voting(True)
    return redirect(reverse('manage'))

@login_required
@transaction.atomic
def disable_voting(request):
    current_round().toggle_voting(False)
    return redirect(reverse('manage'))
    
def get_photo(request, cid):
    entry = get_object_or_404(Candidate, id=cid)
    if not entry.picture:
        raise Http404
    content_type = guess_type(entry.picture.name)
    return HttpResponse(entry.picture, content_type=content_type)

@transaction.atomic
def vote(request):
    if not 'round' in request.POST or not request.POST['round']:
        return error(request, 'Argument "round" is missing in request')
    try:
        r = int(request.POST['round'])
    except:
        return error(request, 'Error parsing argument "round"')
    cr = current_round()
    if not cr.open:
        return error(request, 'Sorry, the vote for this round is currently not open.', redirect = False)
    if r != cr.round:
        return error(request, 'Current round is now round ' + str(cr.round))
    sessionid = request.COOKIES['csrftoken']
    if r == 1:
        try:
            session = Session.objects.get(sessionid = sessionid)
            if session.first_voted:
                return error(request, 'You have voted.', redirect_url = 'a_random_page_that_probably_does_not_exist')
        except ObjectDoesNotExist:
            session = Session(sessionid = sessionid)
        pairs = CandidatePair.objects.all()
        votes = []
        for pair in pairs:
            pid = str(pair.id)
            if not pid in request.POST or not request.POST[pid]:
                return error(request, 'Missing pair #' + pid + 'in request')
            try:
                candidate = Candidate.objects.get(name = request.POST[pid])
                if candidate.id != pair.first.id and candidate.id != pair.second.id:
                    return error(request, "Candidate " + candidate.name + " does not belong to pair " + pid, reverse('home'))
            except ObjectDoesNotExist:
                return error(request, 'Candidate ' + request.POST[pid] + ' does not exist')
            votes.append(candidate)
        for candidate in votes:
            candidate.vote_first_round()
        session.first_voted = True
        session.save()
    elif r == 2:
        try:
            session = Session.objects.get(sessionid = sessionid)
            if session.second_voted:
                return error(request, 'You have voted.', redirect_url = reverse('troll'))
        except ObjectDoesNotExist:
            session = Session(sessionid = sessionid)
        if not 'first_choice' in request.POST or not request.POST['first_choice'] \
            or not 'second_choice' in request.POST or not request.POST['second_choice'] \
            or not 'third_choice' in request.POST or not request.POST['third_choice']:
            return error(request, "first/second/third choice is missing in request")
        try:
            first = Candidate.objects.get(name = request.POST['first_choice'])
            second = Candidate.objects.get(name = request.POST['second_choice'])
            third = Candidate.objects.get(name = request.POST['third_choice'])
            if first.id == second.id or second.id == third.id or first.id == third.id:
                return error(request, "Cannot select the same candidate more than once")
            first.votes_second_round = first.votes_second_round + 5
            second.votes_second_round = second.votes_second_round + 3
            third.votes_second_round = third.votes_second_round + 1
            first.save()
            second.save()
            third.save()
        except ObjectDoesNotExist:
            return error(request, "Candidate does not exist")
        session.second_voted = True
        session.save()
    return render(request, 'success.html')

def troll(request):
    return render(request, 'troll.html')
