from django.contrib import admin

from .models import (
    ChoiceGroup, Choice, Flows, FormElement, FormsGroup,
    FormElement, Guest, ValueElement)


class FormsGroupInline(admin.TabularInline):
    model = FormsGroup
    fields = ('display_order', 'name', 'is_public',)


@admin.register(Flows)
class FlowsAdmin(admin.ModelAdmin):
    fields = ('owner','name','slug','token','is_public',)
    inlines = (FormsGroupInline,)


class FormElementInline(admin.TabularInline):
    model = FormElement
    fields = ('display_order', 'name', 'is_public',)


@admin.register(FormsGroup)
class FormsGroupAdmin(admin.ModelAdmin):
    fields = ('flow','name','slug','display_order','is_public',)
    inlines = (FormElementInline,)


admin.site.register(ChoiceGroup)
admin.site.register(Choice)
admin.site.register(FormElement)
admin.site.register(ValueElement)

admin.site.register(Guest)
