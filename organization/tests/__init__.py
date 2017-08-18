import factory
from django.contrib.auth.models import User
from organization.models import IFrame, Organization


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    email = factory.Faker('email')
    password = factory.Faker('password')
    username = factory.Faker('name')


class OrganizationFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Organization

    title = factory.Faker('company')

    @factory.post_generation
    def user(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.user.add(group)


class IFrameFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = IFrame

    title = factory.Faker('company')
    organization = factory.SubFactory(OrganizationFactory)

