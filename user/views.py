from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy

from tictactoe.models import Game


@login_required
def home(request):
    my_games = Game.objects.games_for_user(request.user)
    active_games = my_games.filter(status='A')
    finished_games = my_games.exclude(status='A')
    waiting_games = active_games.filter(next_to_move=request.user)
    other_games = active_games.exclude(next_to_move=request.user)
    invitations = request.user.invitations_received.all()
    context = {
        'other_games': other_games,
        'waiting_games': waiting_games,
        'finished_games': finished_games,
        'invitations': invitations
    }
    return render(request, 'user/home.html', context)

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'user/signup.html'
    success_url = reverse_lazy('user_home')
