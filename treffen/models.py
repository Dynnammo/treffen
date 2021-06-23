from django.db import models
import random


class Player(models.Model):
    WAITING = 'W'
    IS_PLAYING = 'S'
    IS_OUT = 'IO'
    PLAYER_STATUS = [
        (WAITING, 'Waiting'),
        (IS_PLAYING, 'Is playing'),
        (IS_OUT, 'Is out')
    ]
    name = models.CharField(
        max_length=30,
        blank=True
    )
    picture = models.ImageField(
        upload_to='uploads/',
        null=True,
        blank=True
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
    status = models.CharField(
        max_length=20,
        choices=PLAYER_STATUS,
        default='W'
    )

    def __str__(self):
        return self.name

    def get_next_ziel(self):
        former_ziel = self.ziel
        self.ziel = former_ziel.ziel
        self.mission = former_ziel.mission
        former_ziel.ziel = None
        former_ziel.mission = None
        former_ziel.status = self.IS_OUT
        former_ziel.save()
        self.save()

    # def delete(self, *args, **kwargs):
    #     storage, path = self.picture.storage, self.picture.path
    #     super(Player, self).delete(*args, **kwargs)
    #     storage.delete(path)


class Game(models.Model):
    BATTLE_ROYALE = 'BR'
    COOPERATION = 'CO'
    CHAMPIONSHIP = 'CH'
    GAME_MODES = [
        (BATTLE_ROYALE, 'Battle Royale'),
        (COOPERATION, 'Cooperation'),
        (CHAMPIONSHIP, 'Championship')
    ]
    WAITING_TO_START = 'WTS'
    STARTED = 'S'
    PAUSED = 'P'
    OVER = 'O'
    GAME_STATUS = [
        (WAITING_TO_START, 'Waiting to start'),
        (STARTED, 'Started'),
        (PAUSED, 'Paused'),
        (OVER, 'Over')
    ]
    name = models.CharField(
        max_length=20,
        blank=True,
    )
    type = models.CharField(
        max_length=20,
        choices=GAME_MODES,
        default='BR'
    )
    mission_set = models.ManyToManyField(
        'Mission',
        related_name='affected_games'
    )
    status = models.CharField(
        max_length=20,
        choices=GAME_STATUS,
        default='W'
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.players.count() < 2:
            self.status = self.WAITING_TO_START
        elif self.mission_set.count() < self.players.count():
            self.status = self.WAITING_TO_START
        else:
            if self.status == self.STARTED and self.has_not_started():
                self.start()
        return super().save(*args, **kwargs)

    def start(self, *args, **kwargs):
        self.set_ziele()
        self.set_players_code()

    def set_ziele(self):
        players = [p for p in self.players.all()]
        missions = [m for m in self.mission_set.all()]
        random.shuffle(players)
        random.shuffle(missions)
        index = len(players)-1
        current_player = players[index]
        while not current_player.ziel:
            index -= 1
            current_player.ziel = players[index]
            current_player.mission = missions[index]
            current_player = current_player.ziel
        [p.save() for p in players]
        return

    def set_players_code(self):
        codes = random.sample(range(1000, 9999), self.players.count())
        for player, code in zip(self.players.all(), codes):
            player.player_code = code
            player.save()

    def has_not_started(self):
        for player in self.players.all():
            if player.ziel is not None:
                return False
        return True

    def check_if_finished(self):
        players_remaining_count = 0
        for player in self.players.all():
            if player.ziel:
                players_remaining_count += 1
        if players_remaining_count == 1:
            self.status = self.OVER
        self.save()


class Mission(models.Model):
    name = models.CharField(
        max_length=30
    )
    description = models.TextField(
        max_length=180
    )

    def __str__(self):
        return self.name
