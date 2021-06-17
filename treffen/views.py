from django.views.generic import FormView, TemplateView
from .forms import RegistrationForm
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
            game_id=Game.objects.get(name=form.cleaned_data['game_name']).id
        )
        response.set_cookie('player_id', p.id)
        return response


class WaitingView(TemplateView):
    template_name = "waiting.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = Player.objects.get(id=self.request.COOKIES['player_id'])
        context["player"] = player
        return context
