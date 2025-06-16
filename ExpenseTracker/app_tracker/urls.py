from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/',views.login_view, name= 'login'),
    path('expenses', views.ExpensesListView.as_view(), name = "expenses"), #a CBV
]