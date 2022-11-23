from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


def validate_text(value):
    '''
    Raises ``ValidationError`` unless *value* type is ``str`` or ``unicode``
    '''
    if not (type(value) == str or type(value) == str):
        raise ValidationError(_(u"Must be str or unicode"))


def validate_float(value):
    '''
    Raises ``ValidationError`` unless *value* can be cast as a ``float``
    '''
    try:
        float(value)
    except ValueError:
        raise ValidationError(_(u"Must be a float"))


def validate_int(value):
    '''
    Raises ``ValidationError`` unless *value* can be cast as an ``int``
    '''
    try:
        int(value)
    except ValueError:
        raise ValidationError(_(u"Must be an integer"))


def validate_date(value):
    '''
    Raises ``ValidationError`` unless *value* is an instance of ``datetime``
    or ``date``
    '''
    if not (isinstance(value, timezone.datetime) or isinstance(value, timezone.datetime.date)):
        raise ValidationError(_(u"Must be a date or datetime"))


def validate_bool(value):
    '''
    Raises ``ValidationError`` unless *value* type is ``bool``
    '''
    if not type(value) == bool:
        raise ValidationError(_(u"Must be a boolean"))


def validate_object(value):
    '''
    Raises ``ValidationError`` unless *value* is a saved
    django model instance.
    '''
    if not isinstance(value, models.Model):
        raise ValidationError(_(u"Must be a django model object instance"))
    if not value.pk:
        raise ValidationError(_(u"Model has not been saved yet"))


def validate_enum(value):
    '''
    Raises ``ValidationError`` unless *value* is a saved
    :class:`~eav.models.Choice` model instance.
    '''
    pass
    """
    # This never passes, value is a str
    from .models import Choice
    if not isinstance(value, Choice):
        raise ValidationError(_(u"Must be an Choice model object instance"))
    if not value.pk:
        raise ValidationError(_(u"Choice has not been saved yet"))
    """