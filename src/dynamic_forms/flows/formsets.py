from django.forms.models import modelformset_factory

from .models import ValueElement
from .forms import DynamicElementForm

FormElementValueFormSet = modelformset_factory(ValueElement, form=DynamicElementForm, extra=0,)