from django import forms

from . import models


class FlowForm(forms.ModelForm):
    class Meta:
        model = models.Flows
        fields = ('name', 'is_public')


class FromGroupForm(forms.ModelForm):
    class Meta:
        model = models.FormsGroup
        fields = ('name', 'display_order','is_public')

    
class FormElementForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['datatype'].widget.attrs['onchange'] = "CheckDataType()"
        self.fields['choice_group'].required = False


    class Meta:
        model = models.FormElement
        fields = (
            'name', 'description', 'datatype', 'required',
            'display_order', 'choice_group', 'is_public'
        )
    
    def clean_choice_group(self):
        choice_group = self.cleaned_data['choice_group']
        datatype = self.cleaned_data['datatype']
        if datatype == models.FormElement.TYPE_ENUM and not choice_group:
           raise forms.ValidationError("Please choose enum group")
        return choice_group


class ChoiceGroupForm(forms.ModelForm):
    class Meta:
        model = models.ChoiceGroup
        fields = '__all__'


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = models.Choice
        fields = '__all__'


class DynamicElementForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['form_element'].initial = self.instance
        self.fields['form_element'].choices = [(self.instance, self.instance)]
        self.build_dynamic_fields()
        
    def build_dynamic_fields(self):
        for field in self.fields:
            if field in ['form_element','guest']:
                continue

            if self.instance.datatype == models.FormElement.TYPE_TEXT and field != 'value_text':
                self.fields[field].widget = forms.HiddenInput()
            elif self.instance.datatype == models.FormElement.TYPE_FLOAT and field != 'value_float':
                self.fields[field].widget = forms.HiddenInput()
            elif self.instance.datatype == models.FormElement.TYPE_INT and field != 'value_int':
                self.fields[field].widget = forms.HiddenInput()
            elif self.instance.datatype == models.FormElement.TYPE_DATE and field != 'value_date':
                self.fields[field].widget = forms.HiddenInput()
            elif self.instance.datatype == models.FormElement.TYPE_BOOLEAN and field != 'value_bool':
                self.fields[field].widget = forms.HiddenInput()
            elif self.instance.datatype == models.FormElement.TYPE_ENUM and field != 'value_choice':
                self.fields[field].widget = forms.HiddenInput()
            elif self.instance.datatype == models.FormElement.TYPE_FILE and field != 'value_file':
                self.fields[field].widget = forms.HiddenInput()

            if self.instance.datatype == models.FormElement.TYPE_ENUM and field == 'value_choice':
                enums = self.instance.get_choices().values_list('id', 'value')
                choices = [('', '-----')] + list(enums)
                self.fields[field].choices = choices

    class Meta:
        model = models.ValueElement
        fields = '__all__'


class ValueElementForm(forms.ModelForm):
    class Meta:
        model = models.ValueElement
        fields = '__all__'


    




    