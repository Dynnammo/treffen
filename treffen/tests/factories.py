from treffen.models import Player, Game, Mission
import pytest
import factory


@pytest.mark.django_db
class MissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Mission

    name = factory.Faker('last_name')
    description = factory.Faker('address')


@pytest.mark.django_db(True)
class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game

    name = factory.Faker('first_name')
    type = 'BR'

    @factory.post_generation
    def mission_set(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for mission in extracted:
                self.mission_set.add(mission)


@pytest.mark.django_db(True)
class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Player

    name = factory.Faker('first_name')
    picture = factory.django.ImageField()
    game = factory.SubFactory(GameFactory)
