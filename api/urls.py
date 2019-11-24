from django.urls import path
from . import views

urlpatterns = [
    path('users', views.users_view, name='api_users'),
    path('add_balance', views.add_balance_view, name='api_add_balance'),
]
