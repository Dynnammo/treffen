from django.urls import path
from .views import RegistrationView, WaitingView, GameView

urlpatterns = [
    path('', RegistrationView.as_view(), name="registration"),
    path('waiting', WaitingView.as_view(), name="waiting_page"),
    path("game", GameView.as_view(), name="game")
]
