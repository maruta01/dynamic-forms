import hashlib

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from sort_order_field import SortOrderField

from .validators import *


class Guest(models.Model):
    ip = models.CharField(max_length=128, blank=True, null=True)
    token = models.CharField(max_length=128, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    def save(self, **kwargs):
        self.token = hashlib.md5(self.ip.encode()).hexdigest()
        super().save(**kwargs)

class Flows(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    is_public = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created']
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("form_detail", kwargs={"slug": self.slug})

    def save(self, **kwargs):
        self.slug = slugify(self.name)+f"_{self.id}"
        super().save(**kwargs)


class Choice(models.Model):
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


class ChoiceGroup(models.Model):
    name = models.CharField(unique=True, max_length=100)
    choice = models.ManyToManyField(Choice, verbose_name="Choice group")

    def __str__(self):
        return self.name

class FormsGroup(models.Model):
    flow = models.ForeignKey(Flows, on_delete=models.CASCADE)
    slug = models.SlugField()
    name = models.CharField(max_length=255)
    display_order = SortOrderField(_("display_order"))
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def save(self, **kwargs):
        self.slug = slugify(self.name)+f"_{self.id}"
        super().save(**kwargs)
    
    def __str__(self):
        return self.name


class FormElement(models.Model):
    TYPE_TEXT = 'text'
    TYPE_FLOAT = 'float'
    TYPE_INT = 'int'
    TYPE_DATE = 'date'
    TYPE_BOOLEAN = 'bool'
    TYPE_ENUM = 'enum'
    TYPE_FILE = 'file'

    DATATYPE_CHOICES = (
        (TYPE_TEXT, "Text"),
        (TYPE_FLOAT, "Float"),
        (TYPE_INT, "Integer"),
        (TYPE_DATE, "Date"),
        (TYPE_BOOLEAN, "True / False"),
        (TYPE_ENUM, "Multiple Choice"),
        (TYPE_FILE, "FILE UPLOAD"),
    )

    form_group = models.ForeignKey(FormsGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=256,
                                   blank=True, null=True,
                                   help_text="Short description")
    slug = models.SlugField()
    datatype = models.CharField(max_length=50,
                                    choices=DATATYPE_CHOICES)
    required = models.BooleanField(default=False)
    display_order = SortOrderField(_("display_order"))
    choice_group = models.ForeignKey(ChoiceGroup, on_delete=models.CASCADE, blank=True, null=True)
    is_public = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order']

    def get_validators(self):
        DATATYPE_VALIDATORS = {
            'text': validate_text,
            'float': validate_float,
            'int': validate_int,
            'date': validate_date,
            'bool': validate_bool,
            'object': validate_object,
            'enum': validate_enum,
        }

        validation_function = DATATYPE_VALIDATORS[self.datatype]
        return [validation_function]

    def clean(self):
        if self.datatype == self.TYPE_ENUM and not self.choice_group:
            raise ValidationError(_("You must set the choice group for multiple choice" \
                u"form element"))

        if self.datatype != self.TYPE_ENUM and self.choice_group:
            raise ValidationError(_(
                u"You can only assign a choice group to multiple choice " \
                u"form element"))

    def get_choices(self):
        if not self.datatype == FormElement.TYPE_ENUM:
            return None
        return self.choice_group.choice.all()
    
    def save(self, **kwargs):
        self.slug = slugify(self.name)+f"_{self.id}"
        super().save(**kwargs)

    def __str__(self):
        return self.name


class ValueElement(models.Model):
    form_element = models.ForeignKey(FormElement, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True)
    value_text = models.TextField(blank=True, null=True)
    value_float = models.FloatField(blank=True, null=True)
    value_int = models.IntegerField(blank=True, null=True)
    value_date = models.DateTimeField(blank=True, null=True)
    value_bool = models.BooleanField(blank=True, null=True)
    value_choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='enum_values')
    value_file = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True, null=True,)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.form_element.datatype == FormElement.TYPE_ENUM and self.value_choice:
            if self.value_choice not in self.form_element.choice_group.choice.all():
                raise ValidationError("Choice not Valid")

    def _get_value(self):
        return getattr(self, 'value_%s' % self.form_element.datatype)
    
    def _set_value(self, new_value):
        setattr(self, 'value_%s' % self.form_element.datatype, new_value)







    

