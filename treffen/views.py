from django.views.generic import FormView, TemplateView, ListView
from .mixins import (
    HasAdminAccessMixin
)
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
from .forms import (
    RegistrationForm,
    ZielValidationForm
)
from .models import Player, Game


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'index.html'
    success_url = 'waiting'

    def form_valid(self, form):
        response = super(RegistrationView, self).form_valid(form)
        p = Player.objects.create(
            name=form.cleaned_data['name'],
            picture=form.cleaned_data['picture'],
            game=Game.objects.get(name=form.cleaned_data['game_name'])
        )
        response.set_cookie('player_id', p.id)
        response.set_cookie('game_id', p.game.id)
        return response


class WaitingView(TemplateView):
    template_name = "waiting.html"

    def get(self, request, *args, **kwargs):
        game = Game.objects.get(id=request.COOKIES['game_id'])
        if game.status == 'S':
            messages.success(self.request, 'Game has just started!')
            url = reverse('game')
            return redirect(url)
        messages.error(self.request, 'Game has not started yet')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = Player.objects.get(id=self.request.COOKIES['player_id'])
        context["player"] = player
        context["game_id"] = player.game.id
        return context


class GameView(FormView):
    template_name = "game.html"
    form_class = ZielValidationForm
    success_url = 'game'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        current_player = Player.objects.get(
            id=self.request.COOKIES['player_id']
        )
        current_game = Game.objects.get(id=self.request.COOKIES['game_id'])
        
        if current_player.status == current_player.IS_OUT:
            messages.warning('You are out of the game')
        
        if current_game.status == current_game.OVER:
            if current_player.ziel is None:
                messages.warning(
                    self.request, 'You are out of the game'
                )
            else:
                messages.warning(
                    self.request, 'You have won the game'
                )
            return redirect(reverse('end_game'))
        return response

    def form_valid(self, form):
        response = super(GameView, self).form_valid(form)
        current_player = Player.objects.get(
            id=self.request.COOKIES['player_id']
        )
        current_game = Game.objects.get(id=self.request.COOKIES['game_id'])

        if current_player.status == current_player.IS_OUT:
            return redirect(reverse("end_game"))

        if form.cleaned_data['player_code'] == current_player.ziel.player_code:
            current_player.get_next_ziel()
            current_game.check_if_finished()
            messages.success(self.request, 'Good job ! Here is your new ziel!')
        else:
            messages.error(
                self.request, 'The code you have entered is wrong 😠'
            )

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["player"] = Player.objects.get(
            id=self.request.COOKIES['player_id']
        )
        context["is_out"] = (context["player"].status == Player.IS_OUT)
        return context


class AdminGameView(HasAdminAccessMixin, ListView):
    model = Player
    template_name = "admin/dashboard.html"

    def get_queryset(self):
        qs = Player.objects.filter(
            game=Game.objects.get(name=self.kwargs['game_name'])
        )

        return qs

    def test_func(self):
        return self.request.user.is_superuser


class EndGameView(TemplateView):
    template_name = "end_game.html"
