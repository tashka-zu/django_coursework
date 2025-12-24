from django import forms
from .models import Mailing, Client

from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['name', 'clients', 'message', 'start_time', 'end_time', 'periodicity']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MailingForm, self).__init__(*args, **kwargs)
        if user and not user.groups.filter(name='Managers').exists():
            self.fields['clients'].queryset = Client.objects.filter(owner=user)
