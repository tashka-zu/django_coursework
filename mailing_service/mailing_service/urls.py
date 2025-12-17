from django.contrib import admin
from django.urls import path, include
from allauth.account.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mailing.urls')),
    path('accounts/', include('allauth.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

