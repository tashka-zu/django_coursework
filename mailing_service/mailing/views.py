from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Message
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import MailingForm
from .models import Mailing, Client
from .services import send_mailing


@require_POST
def send_mailing_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    send_mailing(mailing)
    return redirect('mailing_list')

@method_decorator(cache_page(60 * 15), name='dispatch')
class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    success_url = '/clients/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'mailing/client_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('client_list')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')

class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['title', 'body']
    success_url = '/messages/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'mailing/message_form.html'
    fields = ['subject', 'body']
    success_url = reverse_lazy('message_list')

class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('message_list')

@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    def get_queryset(self):
        if self.request.user.groups.filter(name='Managers').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)

    def test_func(self):
        return self.request.user.is_authenticated

class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = '/mailings/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing_list')

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list')

def index(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status='Запущена').count()
    unique_clients = Client.objects.count()
    return render(request, 'mailing/index.html', {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
    })

class MailingStatisticsView(LoginRequiredMixin, TemplateView):
    template_name = 'mailing/mailing_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.groups.filter(name='Managers').exists():
            mailings = Mailing.objects.all()
        else:
            mailings = Mailing.objects.filter(owner=self.request.user)
        context['mailings'] = mailings
        return context


class BlockUserView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Managers').exists()

    def post(self, request, user_id):
        user = User.objects.get(pk=user_id)
        user.is_active = False
        user.save()
        messages.success(request, f'Пользователь {user.username} заблокирован.')
        return redirect('user_list')
