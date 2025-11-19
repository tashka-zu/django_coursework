from django.contrib.messages import Message
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import MailingForm
from .models import Mailing, Client
from .services import send_mailing

@require_POST
def send_mailing_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    send_mailing(mailing)
    return redirect('mailing_list')

# Client Views
class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'clients'

class ClientCreateView(CreateView):
    model = Client
    template_name = 'mailing/client_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('client_list')

class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'mailing/client_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('client_list')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')

# Message Views
class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'

class MessageCreateView(CreateView):
    model = Message
    template_name = 'mailing/message_form.html'
    fields = ['subject', 'body']
    success_url = reverse_lazy('message_list')

class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'mailing/message_form.html'
    fields = ['subject', 'body']
    success_url = reverse_lazy('message_list')

class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('message_list')

# Mailing Views
class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'

class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing_list')

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