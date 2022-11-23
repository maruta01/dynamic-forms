from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'flows'

urlpatterns = [
    path('flows/', login_required(views.FlowsListView.as_view()), name='flow-list'),
    path('flows/create/',login_required(views.FlowsCreateView.as_view()), name='flow-create'),
    path('flows/delete/<slug:slug>/', login_required(views.FlowsDeleteView.as_view()), name='flow-delete'),
    path('flows/detail/<slug:slug>/', login_required(views.FlowsDetailView.as_view()), name='flow-detail'),

    path('flows/<slug:slug>/group/create/',login_required(views.FormGroupCreateView.as_view()), name='group-create'),
    path('flows/group/<slug:slug>/delete/',login_required(views.FormGroupDeleteView.as_view()), name='group-delete'),
    path('flows/group/<slug:slug>/update/',login_required(views.FormGroupUpdateView.as_view()), name='group-update'),

    path('flows/group/<slug:slug>/element/create/',login_required(views.FormElementCreateView.as_view()), name='element-create'),
    path('flows/element/<slug:slug>/update/',login_required(views.FormElementUpdateView.as_view()), name='element-update'),
    path('flows/element/<slug:slug>/delete/',login_required(views.FormElementDeleteView.as_view()), name='element-delete'),

    path('flows/choice_group/create/',login_required(views.ChoiceGroupCreateView.as_view()), name='choice_group-create'),
    path('flows/choice_group/<int:pk>/update/',login_required(views.ChoiceGroupUpdateView.as_view()), name='choice_group-update'),

    path('flows/choice/create/',login_required(views.ChoiceFormCreateView.as_view()), name='choice-create'),

    path('form/flows/<slug:slug>/',views.FormRegistDetailView.as_view(), name='form-create'),

]