from django.contrib import admin
from .models import (
    Player,
    Game,
    Mission
)

admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Mission)
