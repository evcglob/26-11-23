from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
#dashboard
from django import forms
# ws
#change
class Callm(models.Model):
    direction_choices = [
        ('C2S', 'Client to Server'),
        ('S2C', 'Server to Client'),
    ]

    message_type_id = models.CharField(max_length=100)
    message_id = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    payload = models.TextField()

    charger_id = models.CharField(max_length=100, default='')
    sent_at = models.DateTimeField(auto_now_add=True, blank=True)
    direction = models.CharField(max_length=3, choices=direction_choices, blank=True)

    call_result_obj = models.OneToOneField('CallResultm', on_delete=models.CASCADE, null=True)

class CallResultm(models.Model):
    direction_choices = [
        ('C2S', 'Client to Server'),
        ('S2C', 'Server to Client'),
    ]

    message_type_id = models.IntegerField()
    message_id = models.CharField(max_length=36)
    payload = models.TextField()

    charger_id = models.CharField(max_length=100, default='')
    sent_at = models.DateTimeField(auto_now_add=True, blank=True)
    direction = models.CharField(max_length=3, choices=direction_choices, blank=True)

    call_obj = models.OneToOneField('Callm', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'({self.id}) {"Accepted" if "Accepted" in self.payload or len(self.payload) == 2 else "Rejected"}'
#change

# app

class Profile(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    mobile =models.CharField(max_length=20)
    otp = models.CharField(max_length=6)


class Review(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.rating} stars"



#mohammed

class Addmoney(models.Model):
    amount = models.FloatField(max_length=100, default=0, blank=True, null=True)
    final_amount = models.FloatField(max_length=100, default=0, blank=True, null=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=100, null=True, blank=True)
    # user = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    

    def __str__(self):
        return str(self.user)
    

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True, max_length=15)
 
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')
 
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.profile.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user


#===================================================END================================================================================




#dashboard


class ChargingStations(models.Model):
    #general info    
    Charging_Station_Name = models.CharField(max_length=200, default="")
    Address = models.CharField(max_length=200, default="")
    City = models.CharField(max_length=200, default="")
    Zip_Code = models.IntegerField(null=True)
    State = models.CharField(max_length=200, default="")
    Country = models.CharField(max_length=200, default="")
    station_type = models.CharField(max_length=100, default="")
    open = models.CharField(max_length=100, default="")
    Phone_Number = models.CharField(max_length=200, default="")

    #Chrging Point
    Socket_URL = models.CharField(max_length=200, default="")
    Charging_Point_Name = models.CharField(max_length=200, default="")
    Charging_Point_ID = models.CharField(max_length=200, default="")
    Connector_Type = models.CharField(max_length=200, default="")
    Charging_Power = models.CharField(max_length=200, default="")
    EV_Compatible = models.CharField(max_length=200, default="")
    Cost_per_Unit = models.CharField(max_length=200, default="")
    LICENSE = models.CharField(max_length=200, default="")
    Change_Availability = models.CharField(max_length=200, default="")

    #ChargingPoints
    Online_Status = models.CharField(max_length=200, default="")
    Connectors = models.CharField(max_length=200, default="")

    
    Food_Drink = models.CharField(max_length=200)
    Things_to_Do = models.CharField(max_length=200)
    Shopping = models.CharField(max_length=200)
    Services = models.CharField(max_length=200)
    

    def __str__(self):
        return self.Charging_Station_Name
    