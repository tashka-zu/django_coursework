from django.contrib.auth import get_user_model
from django.contrib.messages import Message
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import MailingForm
from .models import Mailing, Client, Message
from .services import send_mailing, send_confirmation_email

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

    def post(self, request, *args, **kwargs):
        mailing_id = request.POST.get('mailing_id')
        mailing = Mailing.objects.get(id=mailing_id)

        # Получаем список клиентов для рассылки
        clients = mailing.recipients.all()

        # Отправляем письма
        for client in clients:
            subject = mailing.message.subject
            message = mailing.message.body
            recipient_list = [client.email]

            send_confirmation_email(subject, message, recipient_list)

        return redirect('mailing_list')

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

User = get_user_model()

def register_user(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            email=request.POST['email'],
            password=request.POST['password']
        )
        send_confirmation_email(user)
        return redirect('login')
    return render(request, 'mailing/register.html')