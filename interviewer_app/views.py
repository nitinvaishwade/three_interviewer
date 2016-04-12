from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from interviewer_app.models import Candidate, Score
from django.http import HttpResponseBadRequest
from django.db.models import Sum
# Create your views here.


@login_required(login_url="/login")
def dashboard(request, template="dashboard_main.html"):
    """
    Render the account detail view page
    """
    all_candidates = Candidate.objects.all()

    return render(request, template, {"all_candidates": all_candidates})


def login_view(request , template="login.html"):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        next_page = request.GET.get('next')
        if user is not None:
            if user.is_active:
                login(request, user)
                if not next_page:
                    next_page = '/scoring/dashboard/'
                return HttpResponseRedirect(next_page)
            else:
                messages.add_message(request, messages.ERROR, "User is Disabled")
        else:
            messages.add_message(request, messages.ERROR, "Invalid User")
        return render(request, template)
    else:
        return render(request, template)


def signup_view(request , template="signup.html"):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            email = request.POST.get('email')
            new_user = User.objects.create_user(first_name=first_name, email=email, username=username, password=password, last_name=last_name)
            return HttpResponseRedirect('/login')
        except:
            messages.add_message(request, messages.ERROR, "Error Creating User Please try again.")
            return render(request, template)
    else:
        return render(request, template)


@login_required(login_url="/login")
def add_candidate(request, template="add_candidate.html"):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        try:
            new_candidate = Candidate.objects.create(email=email, first_name=firstname, last_name=lastname)
        except:
            messages.add_message(request, messages.ERROR, "Unable to create candidate, Please try with different email")

    return render(request, template)


@login_required(login_url="/login")
def rate_candidate(request, candidate_id=None, template="rate_candidate.html"):
    """
    Render the account detail view page
    """
    if not candidate_id:
        return HttpResponseBadRequest

    candidate_detail = get_object_or_404(Candidate, pk=candidate_id)
    score_details = Score.objects.filter(candidate=candidate_detail, interviwer=request.user).first()

    if request.method == "POST":
        score = request.POST.get('score')
        if score_details:
            score_details.score = int(score)
            score_details.save()
        else:
            score_details = Score.objects.create(candidate=candidate_detail, interviwer=request.user, score=int(score))

    score_details = Score.objects.filter(candidate=candidate_detail, interviwer=request.user).first()
    return render(request, template, {"candidate": candidate_detail, "score_detail": score_details})


@login_required(login_url="/login")
def get_results(request, template="get_results.html"):
    credintials_pass = False
    if request.method == "POST":
        username1 = request.POST.get("username1")
        password1 = request.POST.get("password1")
        username2 = request.POST.get("username2")
        password2 = request.POST.get("password2")
        username3 = request.POST.get("username3")
        password3 = request.POST.get("password3")

        user1 = User.objects.filter(username=username1).first()
        if user1:
            if not user1.check_password(password1):
                messages.add_message(request, messages.ERROR, "Passowrd for interviewer 1 is incorrect.Please try again.")
                return render(request, template)
        else:
            messages.add_message(request, messages.ERROR, "Interviewer 1 doesnot exist. Please try again")
            return render(request, template)

        user2 = User.objects.filter(username=username2).first()
        if user2:
            if not user2.check_password(password2):
                messages.add_message(request, messages.ERROR, "Passowrd for interviewer 2 is incorrect.Please try again.")
                return render(request, template)
        else:
            messages.add_message(request, messages.ERROR, "Interviewer 2 doesnot exist. Please try again")
            return render(request, template)

        user3 = User.objects.filter(username=username3).first()
        if user3:
            if not user3.check_password(password3):
                messages.add_message(request, messages.ERROR, "Passowrd for interviewer 3 is incorrect.Please try again.")
                return render(request, template)
        else:
            messages.add_message(request, messages.ERROR, "Interviewer 3 doesnot exist. Please try again")
            return render(request, template)
        credintials_pass = True

    sorted_candidates = {}
    if credintials_pass == True:
        all_candidates = Candidate.objects.all()
        for candidate in all_candidates:
            candidate.total_score = Score.objects.filter(candidate=candidate).aggregate(Sum('score')).get('score__sum', 0)
            candidate.save()
        sorted_candidates = Candidate.objects.all().order_by("-total_score")

    return render(request, template, {"candidates": sorted_candidates})
