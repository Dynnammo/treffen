from django.urls import path
from .views import RegistrationView, WaitingView

urlpatterns = [
    path('', RegistrationView.as_view(), name="registration"),
    path('waiting', WaitingView.as_view(), name="waiting_page")
]
