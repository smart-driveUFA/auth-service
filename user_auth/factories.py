import factory

from user_auth.models import UserModel


class UserFactory(factory.django.DjangoModelFactory):
    username = 'testuser'
    email = factory.Sequence(lambda n: f'testuser{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = UserModel


class SuperUser(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: "superuser%d" % n)
    password = factory.Sequence(lambda n: "7859375jehfwe%d" % n)
    email = factory.Sequence(lambda n: f"superuser{n}@example.com")
    is_superuser = True
    is_active = True
    is_staff = True

    class Meta:
        model = UserModel
