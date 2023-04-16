from django.urls import path

from core.views import CreateAccountView, LoginView

urlpatterns = [
    path('signup', CreateAccountView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
]
