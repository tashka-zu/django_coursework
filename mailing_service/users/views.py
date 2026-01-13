from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('mailing:index')
    template_name = 'users/register.html'

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('mailing:index')

class CustomLogoutView(LogoutView):
    next_page = '/'

class ProfileView(UpdateView):
    model = User
    fields = ['email', 'first_name', 'last_name']
    template_name = 'users/profile.html'
    success_url = reverse_lazy('mailing:index')

    def get_object(self):
        return self.request.user
