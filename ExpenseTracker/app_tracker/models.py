from django.db import models
from datetime import datetime, date

class Account(models.Model):
    name = models.CharField(max_length=100)         
    expense = models.FloatField(default=0)              
    user =  models.ForeignKey('auth.User', on_delete=models.CASCADE) # a user can have many Accounts, but an Account belongs to one user
    expense_list = models.ManyToManyField('Expense',blank = True) # blank=True allows the field to be optional, meaning an account can exist without any expenses associated with it

    def __str__(self):
        return self.name
class Expense(models.Model):    
    name = models.CharField(max_length=100)
    amount = models.FloatField(default=0)
    date = models.DateField(null = False, default=datetime.now)
    long_term = models.BooleanField(default=False)
    interest_rate = models.FloatField(null = True, default=0,blank = True) #can be blank and if it is it will store "" in the database
    end_date = models.DateField(null=True, blank=True)
    monthly_expenses= models.FloatField(null=True,blank=True,default=0)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.long_term:
            self.monthly_expenses = self.calculate_monthly_expense()         
        super().save(*args, **kwargs)   #calls the save in models.Model

    def calculate_monthly_expense(self):
        if self.long_term and self.end_date:
            total_months = (self.end_date.year - self.date.year) * 12 + (self.end_date.month - self.date.month)
            if total_months <= 0:
                return 0
            if self.interest_rate == 0:
                return self.amount / total_months
            else:
                monthly_rate = self.interest_rate / 12 / 100
                return (self.amount * monthly_rate) / (1 - (1 + monthly_rate) ** -total_months) #loan amortization formula
        return round(self.monthly_expenses,2)
    
    def __str__(self):
        return self.name 