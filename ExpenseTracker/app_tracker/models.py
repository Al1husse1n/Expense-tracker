from django.db import models
from datetime import datetime

class Account(models.Model):
    name = models.CharField(max_length=100)
    expense = models.FloatField(default=0)
    user =  models.ForeignKey('auth.User', on_delete=models.CASCADE) #a user can have many Accounts, but an Account belongs to one user
    expense_list = models.ManyToManyField('Expense',blank = True) #blank=True allows the field to be optional, meaning an account can exist without any expenses associated with it

    def __str__(self):
        return self.name
class Expense(models.Model):    
    name = models.CharField(max_length=100)
    amount = models.FloatField(default=0)
    date = models.DateField(null = False, default=datetime.now().date())
    long_term = models.BooleanField(default=False)
    interest_rate = models.FloatField(null = True, default=0,blank = True)
    end_date = models.DateField(null=True, blank=True)
    monthly_expenses= models.FloatField(null=True,blank=True,default=0)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.long_term:
            self.monthly_expenses = calculate_monthly_expense
            super(Expenses,self).save(*args, **kwargs)

    def calculate_monthly_expense(self):
        if self.long_term:
            if self.interest_rate == 0:
                return self.amount/ ((self.end_date - self.date)/30)
            else:
                months = (self.end_date.year - datetime.now().year) * 12 + self.end_date.month - datetime.now().month
                monthly_rate = self.interest_rate/12/100
                monthly_expense = (self.amount * monthly_rate) / (1-(1 + monthly) **-months)
        else:
            return self.monthly_expense
    
