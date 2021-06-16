from django.db import models


class Player(models.Model):
    name = models.CharField(
        max_length=30,
        blank=True
    )
    picture = models.ImageField(
        upload_to='uploads/',

    )
    player_code = models.CharField(
        max_length=10,
        blank=True
    )
    ziel = models.OneToOneField(
        'self',
        on_delete=models.CASCADE,
        related_name='jaeger',
        blank=True,
        null=True
    )
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
        related_name='players'
    )
    mission = models.ForeignKey(
        'Mission',
        on_delete=models.CASCADE,
        related_name='affected_players',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        storage, path = self.picture.storage, self.picture.path
        super(Player, self).delete(*args, **kwargs)
        storage.delete(path)

class Game(models.Model):
    GAME_MODES = [
        ('BR', 'Battle Royale'),
        ('CO', 'Cooperation'),
        ('CH', 'Championship')
    ]
    name = models.CharField(
        max_length=20,
        blank=True,
    )
    type = models.CharField(
        max_length=2,
        choices=GAME_MODES,
        default='BR'
    )
    mission_set = models.ManyToManyField(
        'Mission',
        related_name='affected_games'
    )

    def __str__(self):
        return self.name


class Mission(models.Model):
    name = models.CharField(
        max_length=30
    )
    description = models.TextField(
        max_length=180
    )

    def __str__(self):
        return self.name
