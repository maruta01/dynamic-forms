from secrets import choice
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from jamesite.factories.flows import (
    ChoiceFactory, ChoiceGroupFactory, FlowsFactory,
    ValueElementFactory, FormElementFactory, FormsGroupFactory)
from ..models import Choice, FormElement


class FlowTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_created_flow_should_date_correctly(self):
        flow = FlowsFactory(owner=self.user, name="flow test")
        flow.save()
        assert flow.owner == self.user
        assert flow.name == "flow test"
        assert flow.slug == f"flow-test_{flow.id}"
        assert flow.is_public


class FormsGroupTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.flow = FlowsFactory(owner=self.user)
        self.form_group = FormsGroupFactory(flow=self.flow, name="group test", display_order=1)
        self.flow.save()
        self.form_group.save()

    def test_created_form_group_should_date_correctly(self):
        assert self.form_group.flow == self.flow
        assert self.form_group.name == "group test"
        assert self.form_group.display_order == 1
        assert self.form_group.slug == f"group-test_{self.form_group.id}"
        assert self.form_group.is_public


class FormElementTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.flow = FlowsFactory(owner=self.user)
        self.form_group = FormsGroupFactory(flow=self.flow)
        self.form_element = FormElementFactory(form_group=self.form_group, name="form test", display_order=1)

        self.flow.save()
        self.form_group.save()
        self.form_element.save()
    
    def test_created_form_element_dont_have_choice_should_date_correctly(self):
        assert self.form_element.form_group == self.form_group
        assert self.form_element.name == "form test"
        assert self.form_element.datatype == FormElement.TYPE_TEXT
        assert self.form_element.display_order == 1
        assert self.form_element.slug == f"form-test_{self.form_element.id}"
        assert not self.form_element.choice_group
        assert self.form_element.is_public

    def test_created_form_element_have_choice_should_date_correctly(self):
        choice_1 = ChoiceFactory()
        choice_2 = ChoiceFactory()
        choice_group = ChoiceGroupFactory()
        choice_group.choice.add(choice_1)
        choice_group.choice.add(choice_2)
        form_element = FormElementFactory(
            form_group=self.form_group, name="form choice", datatype=FormElement.TYPE_ENUM,
            display_order=2, choice_group=choice_group)

        choice_1.save()
        choice_2.save()
        choice_group.save()
        form_element.save()

        assert form_element.form_group == self.form_group
        assert form_element.name == "form choice"
        assert form_element.display_order == 2
        assert form_element.slug == f"form-choice_{form_element.id}"
        assert form_element.choice_group == choice_group
        assert form_element.is_public
        assert list(form_element.get_choices()) == [choice_1, choice_2]


class ChoiceGroupTest(TestCase):
    def setUp(self):
        self.choice_1 = ChoiceFactory()
        self.choice_2 = ChoiceFactory()
        self.choice_group = ChoiceGroupFactory(name="choice_group")
        self.choice_group.choice.add(self.choice_1)
        self.choice_group.choice.add(self.choice_2)

        self.choice_1.save()
        self.choice_2.save()
        self.choice_group.save()
    
    def test_created_choice_group_should_date_correctly(self):
        assert self.choice_group.name =="choice_group"
        assert list(self.choice_group.choice.all()) == [self.choice_1, self.choice_2]


class ChoiceTest(TestCase):
    def setUp(self):
        self.choice_1 = ChoiceFactory()
        self.choice_2 = ChoiceFactory()

        self.choice_1.save()
        self.choice_2.save()
    
    def test_created_choice_should_date_correctly(self):
        choice_all = Choice.objects.all()
        list(choice_all) == [self.choice_1, self.choice_2]


class ValueElementTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.flow = FlowsFactory(owner=self.user)
        self.form_group = FormsGroupFactory(flow=self.flow)
        self.form_element = FormElementFactory(form_group=self.form_group)
        
    def test_created_value_element_should_data_correclty(self):
        value_element = ValueElementFactory(form_element=self.form_element, value_text='test')
        value_element.save()
        assert value_element.value_text == "test"
    
    def test_validate_if_enum_type_but_select_choice_other_choice_group_should_raise_error(self):
        choice_1 = ChoiceFactory()
        choice_2 = ChoiceFactory()
        
        choice_group = ChoiceGroupFactory()
        choice_group.choice.add(choice_1)
        choice_group.choice.add(choice_2)
        form_element_enum = FormElementFactory(
            form_group=self.form_group, name="form choice", datatype=FormElement.TYPE_ENUM,
            display_order=2, choice_group=choice_group)

        choice_1.save()
        choice_2.save()
        choice_group.save()
        form_element_enum.save()

        choice_3 = ChoiceFactory()
        choice_3.save()

        value_element = ValueElementFactory(form_element=form_element_enum, value_choice=choice_3)
        
        with self.assertRaises(ValidationError):
            value_element.clean()

    def test_value_element_should_enum_type_should_data_correclty(self):
        choice_1 = ChoiceFactory()
        choice_2 = ChoiceFactory()
        
        choice_group = ChoiceGroupFactory()
        choice_group.choice.add(choice_1)
        choice_group.choice.add(choice_2)
        form_element_enum = FormElementFactory(
            form_group=self.form_group, name="form choice", datatype=FormElement.TYPE_ENUM,
            display_order=2, choice_group=choice_group)

        choice_1.save()
        choice_2.save()
        choice_group.save()
        form_element_enum.save()

        value_element = ValueElementFactory(form_element=form_element_enum, value_choice=choice_2)
        value_element.save()

        assert value_element.value_choice == choice_2
