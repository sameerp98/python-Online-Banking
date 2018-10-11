from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import auth
from django.template.context_processors import csrf
from db.models import Account,History,Loan
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime
#Verification of various fields is implemented
class HomePageView(TemplateView):
    def get(self,request,**kwargs):
        return render(request,'db/login')
def login (request):
    #c={}
    #c.update(csrf(request))
    return render(request,'login.html')
def auth_view (request):
    username= request.POST.get('username','')
    password= request.POST.get('password','')
    user= auth.authenticate (request,username=username,password=password)
    if user is not None :
        auth.login (request,user)#creates session and user ID in the request
        #request.session['username']=username
        try:
            Account.objects.get(clients_id=user)
            return HttpResponseRedirect('/db/loggedin')
        except:
            c={'msg':'Enter correct information',}
            return HttpResponseRedirect('/db/login',c)
    else:
        return HttpResponseRedirect('/db/invalidlogin')
@login_required(login_url="/db/login/")
def loggedin (request):
    op=request.POST.get('operation',default=False)
    #uname=request.session['username']
    if(op):
        if(op=="transaction"):
            return HttpResponseRedirect('/db/transaction_create')
        elif (op=="balance"):
            c={'msg':Account.objects.filter(clients_id=request.user)[0],
               "fullname":request.user.username ,
                }
            return render(request,'loggedin.html',c)
        elif(op=="history"):#add entries to the history table first
            c={'history_table':History.objects.filter(client_id=request.user),}
            return render(request,'loggedin.html',c)
        elif(op=="loan"):
            return HttpResponseRedirect("/db/loan")
    else:
        return render(request,'loggedin.html',{"fullname":request.user.username})
@login_required(login_url="/db/login/")
def transaction_create(request):
    c={'from_ac' : Account.objects.get(clients_id=request.user).acc_no,}
    return render(request,'transaction_create.html',c)    
@login_required(login_url="/db/login/")
def do_transaction (request):#check to_ac , amount value >0 <total,50000     
        to_ac = request.POST.get('to_ac','')#string
        amount= request.POST.get('amount','')#string
        if(request.POST.get('to_ac','')=='' or request.POST.get('amount','')==''):
            c={'msg':'Enter all fields','from_ac' : Account.objects.get(clients_id=request.user).acc_no,}
            return render (request,'transaction_create.html',c)
        try:
            to_acc_int=int(to_ac)
            amount_float=float(amount)
            to_account=Account.objects.get(acc_no=to_acc_int)
            from_account=Account.objects.get(clients_id=request.user)    
            if (not amount.isdigit()):
                c={'msg':'Enter Valid amount','from_ac' : Account.objects.get(clients_id=request.user).acc_no,}
                return render(request,'transaction_create.html',c)
            if ((amount_float>0)and (amount_float<=50000)):
                if (amount_float>from_account.acc_balance):
                    c={'msg':'Not enough funds for Transfer','from_ac' : Account.objects.get(clients_id=request.user).acc_no,}
                    return render("transaction_create.html",c)
                to_account.acc_balance+=amount_float
                from_account.acc_balance-=amount_float
                #from now onwards we need to create entries in the history tablec
                histuser=History(client_id=request.user,from_account_no=from_account.acc_no ,to_account_no=to_account.acc_no ,time=datetime.datetime.now() ,amount=amount_float)
                histuser2=History(client_id=to_account.clients_id,from_account_no=from_account.acc_no ,to_account_no=to_account.acc_no ,time=datetime.datetime.now() ,amount=amount_float)
                histuser.save()
                histuser2.save()
                to_account.save()
                from_account.save()
                return render (request,'loggedin.html',{'msg':'Transaction successful!','fullname':request.user.username})
        except:
            c={'msg':'Enter Correct Details (Check Account number)','from_ac' : Account.objects.get(clients_id=request.user).acc_no, }
            return render(request,'transaction_create.html',c)                
            
@login_required(login_url="/db/login/")
def loan(request):
    if (request.POST.get('amount','')==''and request.POST.get('duration','')==''):
        return render (request,'loan.html',{'msg':'Enter valid details'})
    amount = request.POST.get('amount')
    duration=request.POST.get('duration')
    if(not amount.isdigit() or not duration.isdigit() or float(amount)<0 or float(duration)<0):
        return render (request,'loan.html',{'msg':'Enter valid numbers',})
    else:
        try:
            duration_float=float(duration)
            time = datetime.datetime.now() + datetime.timedelta(days=(365*duration_float))
            amount_float=float(amount)
            new_loan=Loan(clients_id=request.user,loan_amount=amount_float,loan_interest=7.00,loan_duration=time)
            user_acc= Account.objects.get(clients_id=request.user)
            user_acc.acc_balance+=amount_float
            user_acc.save()
            new_loan.save()
            return render(request,'loggedin.html',{'msg':'Loan creation successfull',"fullname":request.user.username})
        except:
            return render (request,'loan.html',{'msg':'Error in creation of loan Please try agagin.'})
def invalidlogin(request):#complete
    return render(request,'invalidlogin.html')
@login_required(login_url="/db/login/")
def logout (request):#complete
    auth.logout(request)
    return render(request,'logout.html')
