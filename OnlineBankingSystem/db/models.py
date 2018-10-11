from django.db import models
from django.contrib.auth.models import User 
# Create your models here.
"""
class Clients (models.Model):
    first_name = models.CharField(max_length=15)
    last_name =models.CharField(max_length=15)
    clients_id= models.OneToOneField(User, on_delete=models.CASCADE,)
    client_id=models.CharField(max_length=10,primary_key=True,)   
"""
class Account(models.Model):
    clients_id= models.OneToOneField(User, on_delete=models.CASCADE,)
    #client_id= models.ForeignKey('Clients',on_delete=models.CASCADE,)
    acc_no = models.IntegerField(primary_key=True)
    acc_balance =models.FloatField()
    def __str__(self):
        return("Your account balance is "+str(self.acc_balance))
""" This is maintained by django.contrib.auth user
class Login (models.Model):
    client_id = models.ForeignKey('clients',on_delete=models.CASCADE,)
    username=models.CharField(max_length=20,primary_key=True,)
    password=models.CharField(max_length=20)
"""
#class Credit(models.Model):        
#class Debit(models.Model):
class Loan(models.Model):
    clients_id= models.ForeignKey(User, on_delete=models.CASCADE,)
    loan_amount=models.FloatField()
    loan_interest=models.FloatField()
    loan_duration=models.DateTimeField()
class History(models.Model):
    client_id=models.ForeignKey(User,on_delete=models.CASCADE)
    from_account_no= models.IntegerField()
    to_account_no= models.IntegerField()
    time=models.DateTimeField()
    amount=models.FloatField() 