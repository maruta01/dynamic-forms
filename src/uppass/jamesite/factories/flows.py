import factory
from faker import Faker
from factory.django import DjangoModelFactory

from flows.models import (
    Choice, ChoiceGroup, ValueElement,
    Flows, FormElement, FormsGroup, Guest)

fake = Faker()


class FlowsFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: 'flows_%d' % (n))
    is_public = True

    class Meta:
        model = Flows


class FormsGroupFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: 'group_%d' % (n))
    display_order = factory.Sequence(lambda n:(n))
    is_public = True

    class Meta:
        model = FormsGroup


class FormElementFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: 'name_%d' % (n))
    display_order = factory.Sequence(lambda n:(n))
    datatype = FormElement.TYPE_TEXT
    is_public = True

    class Meta:
        model = FormElement


class ChoiceFactory(DjangoModelFactory):
    value = factory.Sequence(lambda n: 'choice_%d' % (n))

    class Meta:
        model = Choice


class ChoiceGroupFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: 'choice_group_%d' % (n))

    class Meta:
        model = ChoiceGroup


class GuestFactory(DjangoModelFactory):
    ip = fake.ipv4(network=True, private=True)
    
    class Meta:
        model = Guest


class ValueElementFactory(DjangoModelFactory):
    guest = factory.SubFactory(GuestFactory)

    class Meta:
        model = ValueElement