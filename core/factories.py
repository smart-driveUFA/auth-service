import factory

from core.models import TPI


class TpiFactory(factory.django.DjangoModelFactory):
    lat_start = factory.Sequence(lambda n: 53.3645 + n)
    lon_start = factory.Sequence(lambda n: 53.6666 + n)
    lat_end = factory.Sequence(lambda n: 54.3645 + n)
    lon_end = factory.Sequence(lambda n: 54.6666 + n)
    start = factory.Sequence(lambda n: f"test_start{n}")
    end = factory.Sequence(lambda n: f"test_end{n}")
    highway = factory.Sequence(lambda n: f"test_highway{n}")

    class Meta:
        model = TPI
