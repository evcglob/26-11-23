from django.contrib import admin
from django.urls import path, include
from api import views


#dadshboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #ws
    path('admin/', admin.site.urls, name='admin'),
    path('trigger-remote-start/', views.trigger_remote_start_transaction, name='trigger-remote-start'),
    path('trigger-remote-stop/', views.trigger_remote_stop_transaction, name='trigger-remote-stop'),


    #app
    path('estimate', views.estimate , name="estimate" ),
    path('stop', views.stop , name="stop" ),
    path('start', views.start , name="start" ),
    path('rating', views.review , name="rating" ),  
    path('razorpayhandler', views.razorpayhandler , name="razorpayhandler" ),  
    path('logout/', views.LogoutView, name='logout'),               
    path('accounts/', include('allauth.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),      
    path("addmoney/", views.addmoney, name="addmoney"),
    path("billinfo", views.billinfo, name="billinfo"),    
    path("razorpayment/", views.razorpayment, name="razorpayment"), 


    path('logindash', views.logindash , name="logindash" ),
    path('dashboard' , views.dashboard , name='dashboard'),
    
    path('newstation' , views.newstation , name='newstation'),
    path('rfid' , views.rfid , name='rfid'),
    path('role' , views.role , name='role'),
    path('user' , views.user , name='user'),  
    path('logs', views.logs , name='logs'),
    
    
    path('register' , views.register , name='register'),
    path('otp' , views.otp, name='otp'),
    path('verify_otp' , views.verify_otp, name='verify_otp'),
    path('' , views.user_login, name='login'),   
    path('error' , views.error, name='error'), 


    #dashboard

    path('station/' , views.station , name='station'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/' , views.delete , name='delete'),
    path('edit/<int:id>/' , views.edit , name='edit'),




    #conditions
    path("privacy", views.privacy, name="privacy"), 
    path("terms", views.terms, name="terms"), 
    path("refund", views.refund, name="refund"), 





    #15/08/2023
    path("apistart", views.API_START, name="API_START"),
    path("apistop", views.API_STOP, name="API_END"),
]

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 
