from django import forms
from .models import Player, Game


class RegistrationForm(forms.ModelForm):
    game_name = forms.CharField(
        max_length=Game.name.field.max_length,
        label="Game name",
        required=True
    )

    class Meta:
        model = Player
        fields = ("name", "picture",)

    def is_valid(self):
        valid = super(RegistrationForm, self).is_valid()
        cleaned_data = self.cleaned_data
        if not cleaned_data['picture'] and not cleaned_data['name']:
            self._errors['Invalid identification'] = (
                'Name or picture must be given'
            )
            return False
        if Game.objects.filter(name=cleaned_data['game_name']).count() == 0:
            self._errors['Invalid game'] = (
                'Game does not exist: please check game name'
            )
            return False
        return valid
