from django.urls.conf import path
from db.views import login,logout,loggedin, invalidlogin,auth_view,transaction_create,do_transaction,loan
#from django.contrib.auth import views as auth_view

urlpatterns = [
    path('login/',login,name='login'),
    path('auth/',auth_view,name='auth_view'),
    path('logout/',logout,name='logout'),
    path('loggedin/',loggedin,name='loggedin'),
    path('invalidlogin/',invalidlogin,name='invalidlogin'),
    path('transaction_create/',transaction_create),
    path('do_transaction/',do_transaction),
    path('loan/',loan)
]
