from django.contrib import admin
from .models import Account,History,Loan
from django.contrib.auth.models import User

admin.site.register(Account)
admin.site.register(History)
admin.site.register(Loan)

# Register your models here.
