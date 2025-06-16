from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Account, Expense
from django.views.generic import TemplateView   #Provides a generic class-based view to render a static or context-driven template
from django.views.generic.edit import FormView  #CBV for forms
from django.views.generic  import ListView      #CBV for displaying list of objects
from datetime import datetime
from .forms import ExpenseForm
from dateutil.relativedelta import relativedelta
from django.utils.safestring import mark_safe
from django.db.models import Sum, Count, F  
import plotly.express as px #pip install plotly
from plotly.graph_objs import *

def home(request):
    return render(request, "home/home.html")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/login.html', {'form':form})

def generate_graph(data):
    
    fig = px.bar(data, x='months', y='expenses', title='Monthly Expenses')
    fig.update_layout(
        xaxis=dict(rangeslider=dict(visible=True)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='rgba(0,0,0,1)',
    )
    fig.update_traces(marker_color='#008c41')

    graph_json = fig.to_json()

    return graph_json

class ExpensesListView(FormView): #provides methods like get(), post(), and form_valid() — you only override what you need.
    template_name = 'app_tracker/expenses_list.html'
    form_class = ExpenseForm
    success_url = "/"

    def form_valid(self, form): #form is the ExpenseForm instance with cleaned and valid data.
        account , _ = Account.objects.get_or_create(user = self.request.user)

        expense = Expense(   #expense = new Expense
            name = form.cleaned_data['name'],
            amount = form.cleaned_data['amount'],
            interest_rate = form.cleaned_data['interest_rate'],
            date = form.cleaned_data['date'],
            end_date = form.cleaned_data['end_date'],
            long_term = form.cleaned_data['long_term'],
            user = self.request.user #self.request.user means the currently logged-in user.
        ) 
        expense.save()
        account.expense_list.add(expense)
        return super().form_valid(form) #Redirect the user to success_url and Do any additional default behavior
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        accounts = Account.objects.filter(user=user) 

        expense_data_graph = {}
        expense_data = {}

        for account in accounts:
            expenses = account.expense_list.all()
            for expense in expenses:
                if expense.long_term and expense.monthly_expenses:
                    current_date = expense.date
                    while current_date <= expense.end_date:
                        year_month = current_date.strftime('%Y-%m')
                        expense_data_graph.setdefault(year_month, []).append({
                            'name': expense.name,
                            'amount': expense.monthly_expenses,
                            'date': expense.date,
                            'end_date': expense.end_date,
                        })
                        current_date += relativedelta(months=1)
                else:
                    year_month = expense.date.strftime('%Y-%m')
                    expense_data_graph.setdefault(year_month, []).append({
                        'name': expense.name,
                        'amount': expense.monthly_expenses,
                        'date': expense.date,
                    })

        aggregated_data = [
            {'year_month': key, 'expense': sum(item['amount'] for item in value)}
            for key, value in expense_data_graph.items()
        ]

        context['expense_data'] = expense_data_graph
        context['aggregated_data'] = aggregated_data
        context['expenses'] = Expense.objects.filter(user=user)  # ✅ Fix added

        graph_data = {
            'months': [item['year_month'] for item in aggregated_data],
            'expenses': [item['expense'] for item in aggregated_data]  # ✅ Fix name
        }
        context['graph_data'] = mark_safe(generate_graph(graph_data))

        return context
