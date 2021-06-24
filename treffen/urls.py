from django.urls import path
from .views import (
    RegistrationView,
    WaitingView,
    GameView,
    AdminGameView,
    EndGameView
)

urlpatterns = [
    path('', RegistrationView.as_view(), name="registration"),
    path('waiting', WaitingView.as_view(), name="waiting_page"),
    path("game", GameView.as_view(), name="game"),
    path(
        "dashboard/<str:game_name>/",
        AdminGameView.as_view(),
        name="admin_game"
    ),
    path("end_game", EndGameView.as_view(), name="end_game"),
]
