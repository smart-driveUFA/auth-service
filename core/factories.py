import factory

from core.models import TPI


class TpiFactory(factory.django.DjangoModelFactory):
    latitude = factory.Sequence(lambda n: 53.3645 + n)
    longitude = factory.Sequence(lambda n: 53.6666 + n)
    direction = factory.Sequence(lambda n: f'test_direction{n}')

    class Meta:
        model = TPI
