from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic


from .forms import  (
    ChoiceForm, ChoiceGroupForm, FlowForm,
    FormElementForm, FromGroupForm, ValueElementForm)
from .models import (
    Choice, ChoiceGroup, Flows, FormElement,
     FormsGroup, Guest)
from .formsets import FormElementValueFormSet


# Flows Group Views
class FlowsListView(generic.ListView):
    model = Flows
    template_name = 'flows/flow_list.html'
    context_object_name = 'flows'

    def get_queryset(self):
        return Flows.objects.filter(owner=self.request.user)


class FlowsCreateView(generic.CreateView):
    model = Flows
    form_class = FlowForm
    template_name = 'flows/flow_create_update.html'
    success_message = _('Flow created successfully')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('flows:flow-detail', kwargs={"slug": self.object.slug})


class FlowsDeleteView(generic.DeleteView):
    model = Flows
    form_class = FlowForm
    context_object_name = 'flow'
    template_name = 'flows/flow_delete.html'
    success_url = reverse_lazy('flows:flow-list')

    def get_success_url(self):
        messages.info(self.request, _("Flow deleted successfully"))
        return reverse_lazy('flows:flow-list')


class FlowsDetailView(generic.DetailView):
    model = Flows
    template_name = 'flows/flow_detail.html'
    context_object_name = 'flow'

    def get_form_groups(self, flow):
        qs = FormsGroup.objects.filter(flow_id=flow).values().order_by("display_order")
        qs_list = [entry for entry in qs]
        result = []
        for list in qs_list: 
            result.append(
                {
                    **list,
                    "elements":FormElement.objects.filter(
                        form_group__id=list.get('id')).values().order_by("display_order")
                }
            )
        return result

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        flow = kwargs.get('object')
        ctx['form_groups'] = self.get_form_groups(flow)
        return ctx


# Form Group Views
class FormGroupCreateView(generic.CreateView):
    model = FormsGroup
    template_name = 'form_groups/form_group_create_update.html'
    form_class = FromGroupForm
    context_object_name = "form_group"
    success_message = _('Flow group created successfully')

    def form_valid(self, form):
        flow = Flows.objects.get(slug=self.kwargs.get('slug'))
        form.instance.flow = flow
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('flows:flow-detail', kwargs={"slug": self.kwargs.get('slug')})


class FormGroupDeleteView(generic.DeleteView):
    model = FormsGroup
    form_class = FromGroupForm
    context_object_name = 'form_group'
    template_name = 'form_groups/form_group_delete.html'
    success_message = _("form group deleted successfully")

    def get_success_url(self):
        messages.info(self.request, self.success_message)
        return reverse_lazy('flows:flow-detail', kwargs={"slug": self.request.GET.get('flow')})


class FormGroupUpdateView(generic.UpdateView):
    model = FormsGroup
    form_class = FromGroupForm
    context_object_name = 'form_group'
    template_name = 'form_groups/form_group_create_update.html'
    success_message = _("form group updated successfully")

    def get_success_url(self):
        messages.info(self.request, self.success_message)
        return reverse_lazy('flows:flow-detail', kwargs={"slug": self.request.GET.get('flow')})


# Form Element Views
class FormElementCreateView(generic.CreateView):
    model = FormElement
    template_name = 'form_elements/form_element_create_update.html'
    form_class = FormElementForm
    context_object_name = "form_element"
    success_message = _('Flow element created successfully')

    def form_valid(self, form):
        form_group = FormsGroup.objects.get(slug=self.kwargs.get('slug'))
        form.instance.form_group = form_group
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy('flows:flow-detail', kwargs={"slug": self.request.GET.get('flow')})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['url_param'] = "?"+self.request.GET.urlencode()+"&form_group="+self.kwargs.get('slug')
        return ctx


class FormElementUpdateView(generic.UpdateView):
    model = FormElement
    template_name = 'form_elements/form_element_create_update.html'
    form_class = FormElementForm
    context_object_name = "form_element"
    success_message = _('Flow element updated successfully')

    def get_success_url(self):
        messages.info(self.request, self.success_message)
        return reverse_lazy('flows:flow-detail', kwargs={"slug": self.request.GET.get('flow')})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['url_param'] = self.request.GET.urlencode()+"?form_group="+self.kwargs.get('slug')
        return ctx


class FormElementDeleteView(generic.DeleteView):
    model = FormElement
    template_name = 'form_elements/form_element_delete.html'
    form_class = FormElementForm
    context_object_name = "form_element"
    success_message = _('Flow element deleted successfully')

    def get_success_url(self):
        messages.info(self.request, self.success_message)
        return reverse_lazy('flows:flow-detail', kwargs={"slug": self.request.GET.get('flow')})


# Form Question Views
class ChoiceGroupCreateView(generic.CreateView):
    model = ChoiceGroup
    template_name = 'choice/choice_group_create_update.html'
    form_class = ChoiceGroupForm
    context_object_name = "choice_group"
    success_message = _('Choice group created successfully')

    def get_success_url(self):
        messages.info(self.request, self.success_message)
        return reverse_lazy(
            'flows:element-create', kwargs={
                "slug": self.request.GET.get('form_group')
            })+"?"+self.request.GET.urlencode()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['url_param'] = self.request.GET.urlencode()
        return ctx


class ChoiceGroupUpdateView(generic.UpdateView):
    model = ChoiceGroup
    template_name = 'choice/choice_group_create_update.html'
    form_class = ChoiceGroupForm
    context_object_name = "choice_group"
    success_message = _('Choice group updated successfully')

    def get_success_url(self):
        messages.info(self.request, self.success_message)
        return reverse_lazy(
            'flows:element-create', kwargs={
                "slug": self.request.GET.get('form_group')
            })+"?"+self.request.GET.urlencode()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['url_param'] = self.request.GET.urlencode()
        return ctx


# Form ChoiceForm Views
class ChoiceFormCreateView(generic.CreateView):
    model = Choice
    template_name = 'choice/choice_create_update.html'
    form_class = ChoiceForm
    context_object_name = "choice"
    success_message = _('choice created successfully')

    def get_success_url(self):
        messages.info(self.request, self.success_message)
        return reverse_lazy('flows:choice_group-create')+"?"+self.request.GET.urlencode()


class FormRegistDetailView(generic.DetailView):
    model = Flows
    form_class: ValueElementForm
    template_name = 'flows/value_element_create_update.html'
    formset_class = FormElementValueFormSet
    success_url = reverse_lazy('flows:flow-list')

    def get_or_create_user(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')

        if not Guest.objects.filter(ip=ip).exists():
            user = Guest.objects.create(ip=ip)
        else:
            user = Guest.objects.get(ip=ip)

        return user

    def get_queryset(self):
        qs = super().get_queryset()
        self.user = self.get_or_create_user()
        return qs

    def get_form_element(self):
        form_group = FormsGroup.objects.filter(flow__slug=self.kwargs.get('slug')).exclude(is_public=False).first()
        elements = FormElement.objects.filter(form_group=form_group).exclude(is_public=False)
        return elements
        
    def get_context_data(self, *arg,**kwargs):
        ctx = super().get_context_data(*arg,**kwargs)
        elements = self.get_form_element()
        ctx['formset'] = self.formset_class(queryset=elements)
        return ctx
