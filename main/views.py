# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .models import Question, Answer, Profile
from .forms import SignupForm, LoginForm
import random


@login_required
def index(request):
    """
    View function for index page.

    Renders index page if session doen't contain IDs.
    Otherwise redirects to 'process' page. This is the
    view that user is redirected to after a successful login.
    """
    shuffled_pks = request.session.get('shuffled_pks')
    if shuffled_pks:
        return redirect('process')
    return render(request, 'main/index.html')


@login_required
def process(request, template_name="main/process.html"):
    """
    View function for process page.

    This functoin is responsible for processing POST requests
    when user submits answers and sends questions to template
    one by one.
    """
    shuffled_pks = request.session.get('shuffled_pks')
    if request.method == 'POST':
        answer_pk = request.POST.get('answer_pk')
        answer = get_object_or_404(Answer, pk=answer_pk)
        shuffled_pks.pop()
        is_empty = len(shuffled_pks) == 0
        if answer.is_correct:
            points = answer.question.points
            request.session['points'] += points
            response = "Your answer is correct. \
                        You earned {} points!".format(points)
        else:
            correct_answer = answer.question.answers.filter(
                is_correct=True
            ).first()
            response = "Your answer is wrong. \
                        The correct answer is: {}".format(correct_answer)

        if is_empty:
            profile = request.user.profile
            if request.session['points'] > profile.points:
                profile.points = request.session['points']
                profile.save()

        context = {
            'response': response,
            'question': answer.question,
            'is_empty': is_empty
        }
        request.session['shuffled_pks'] = shuffled_pks
        return render(request, template_name, context)
    context = {}
    if shuffled_pks:
        question = get_object_or_404(Question, pk=shuffled_pks[-1])
        context = {'question': question}
    return render(request, template_name, context)


def start(request):
    """
    Initialize session with shuffled question IDs.

    This function is called when START or START AGAIN
    buttons are clicked to (re)initialize the session.
    """
    q_count = 2
    question_pks = Question.objects.values_list('pk', flat=True)
    if len(question_pks) < q_count:
        warning = "Not enough questions. Please add more."
        return HttpResponse(warning)
    question_pks = list(question_pks)
    random.shuffle(question_pks)
    request.session['shuffled_pks'] = question_pks[:q_count]
    request.session['points'] = 0
    return redirect('process')


def leaderboard(request):
    """
    Retrieve user profiles to display on leaderboard page.

    Profiles are ordered by descending order of the earned points.
    """
    profiles = Profile.objects.all().order_by('-points')
    return render(request, 'main/leaderboard.html', {'profiles': profiles})


def signup(request):
    """
    Construct username using first name and last name.

    Username uniqueness is enforced by the combination of
    first and last names. Username field is not used on page
    so it's assigned in view to preserve form data integrity.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form_data = form.save(commit=False)
            form_data.username = "{}_{}".format(data['first_name'],
                                                data['last_name']
                                                )
            form_data.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=form_data.username,
                                password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'auth/signup.html', {'form': form})


class CustomLoginView(LoginView):
    """
    Subclass LoginView to set custom attribute values.

    Form class and template name are overriden. User
    is redirected after authentication. Redirect URL
    is set in settings.py LOGIN_REDIRECT_URL variable.
    """

    form_class = LoginForm
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
