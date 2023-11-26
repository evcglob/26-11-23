# ws
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

# app

from django.db.models import Sum
from time import time
from django.core.mail import send_mail
from tokenize import generate_tokens
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from api.models import *
from django.contrib.auth.decorators import login_required
from google.auth.transport import requests
from django.conf import settings
import razorpay
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
import json
import requests
import random
from core.settings import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
from django.utils import timezone
from django.db import IntegrityError
import http.client
from datetime import datetime
import datetime
import pytz

# ================================================================================================================================
# app

#wallteend

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


def update_balance(wallet, payment_amount):
    updated_balance = wallet.balance + payment_amount
    return updated_balance


def LogoutView(request):
    logout(request)
    return redirect('login')



def error(request):
    return render(request, 'error.html')


@login_required
def review(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        review = Review.objects.create(
            name=name, rating=rating, comment=comment)
        review.save()
        reviews = Review.objects.all().order_by('-id')
        count = Review.objects.count()
        return render(request, 'login.html', {'reviews':reviews, 'count':count})
    reviews = Review.objects.all().order_by('-id')
    count = Review.objects.count()
    return render(request, 'rating.html', {'reviews':reviews, 'count':count})


def pay(request):
    return render(request, 'pay.html')


def forgot_password(request):
    if request.method == 'POST':
        # Handle the form submission and send the password reset email
        email = request.POST.get('email')
        # Your code to send the password reset email goes here
        send_mail(
            'Password reset',
            'Click the link to reset your password: https://yourwebsite.com/reset_password',
            'noreply@yourwebsite.com',
            [email],
            fail_silently=False,
        )
        return render(request, 'forgot_password_sent.html')
    return render(request, 'forgot_password.html')

    # def send_otp(request):
    mobile = request.POST.get('mobile')
    otp = str(random.randint(1000, 9999))

    amount = request.POST.get('amount')
    totalbalance = request.POST.get('totalbalance')

    # Send SMS OTP message
    msg = 'EVC Global App Login OTP is ' + otp + \
          '. OTP is valid for 5 minutes. Do not share this with anyone for security reason.'
    url = 'https://www.smsgateway.center/SMSApi/rest/send'
    payload = {
        'userId': 'evcglobal',
        'password': 'Evcglob@l2022',
        'senderId': 'EVCGLO',
        'sendMethod': 'simpleMsg',
        'msgType': 'text',
        'mobile': f'91{mobile}',
        'msg': msg,
        'duplicateCheck': 'true',
        'format': 'json'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'Cookie_1=value; Cookie_2=value'
    }
    response = requests.post(url, headers=headers, data=payload)
    print(response)

    return render(request, 'send_otp.html')

    # def verifyotp(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        otp = request.POST.get('otp')
        if PhoneOTP.objects.filter(mobile=mobile, otp=otp).exists():
            app_user = PhoneOTP.objects.get(mobile=mobile, otp=otp)
            app_user.otp_verified = True
            app_user.save()
            return HttpResponse('OTP Verified')
        else:
            return HttpResponse('Wrong OTP, Please Try Again')
    return render(request, 'verifyotp')

#invoice
from django.db.models import Max

def billinfo(request):
    global chrg_amt
    global input_value
    global gst
    time = round((((chrg_amt/12.5)*60)*1000), 2)
    first_charging_station = ChargingStations.objects.latest('id')
    change_amount = first_charging_station.Cost_per_Unit
    charging_amount_rate = int(change_amount)
    KW = round(chrg_amt/charging_amount_rate, 2)
    print(charging_amount_rate)

    try:
        user = request.user.id
        print(user)
        paymentbill = Addmoney.objects.latest('order_id')
        amountbill = paymentbill.final_amount
        ewalletuser = Addmoney.objects.get(user=user)
        after_charge_balance = ewalletuser.final_amount - input_value
        ewalletuser.final_amount = after_charge_balance
        ewalletuser.save()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    india_timezone = pytz.timezone('Asia/Kolkata')
    current_datetime = datetime.now(india_timezone)
    current_time = current_datetime.strftime('%I:%M %p')
    transaction_id = random.randint(1000000, 99999999)


    
    context = {
        'kwh_value':KW,
        'final_amount_charge_amount':round(KW*charging_amount_rate, 2),
        'current_time':current_time, 
        'transaction_id':transaction_id,
        'gst':gst,
        'total':input_value,      
    }
    return render(request, 'billinfo.html', context)


# payment
@login_required
def addmoney(request):
    return render(request, 'payment.html')

@login_required
@csrf_exempt
def estimate(request):
    # user = int(request.user.id)
    user = request.user.id
    print(user)
    try:
        ewallet = Addmoney.objects.get(user=user)
        balance = ewallet.final_amount
    except Addmoney.DoesNotExist:
        # Handle the case where the user's EWallet does not exist
        balance = 0.00
    context = {
        'balance': balance,
        }
    return render(request, 'estimate.html', context)


input_value = None
@login_required
@csrf_exempt
def start(request):
    global input_value
    global chrg_amt
    global gst
    if request.method == 'POST':
        first_charging_station = ChargingStations.objects.latest('id')
        print(first_charging_station)
        change_amount = first_charging_station.Cost_per_Unit
        charging_amount_rate = int(change_amount)
        print(charging_amount_rate)
        
        input_value = int(request.POST.get("amount"))
        gst = round((input_value*15.25)/100, 2)
        chrg_amt = round(input_value-gst, 2)
        KW = round(chrg_amt/charging_amount_rate, 2)        
        context = {
            'input_value': input_value,
            'gst': gst,
            'chrg_amt': chrg_amt,
            'KW': KW,
            'change_amount':change_amount,
            # 'state_of_charge':second_value,
        }
        return render(request, 'start.html', context)
    return render(request, 'start.html')


def razorpayment(request):
    order = None
    if request.method == 'POST':
        # name = request.POST.get("name")
        user = request.user
        amount = int(request.POST.get("amount")) * 100
        currency = "INR"
        receipt = f"EVC GLOBAL- {int(time())}"
        order = client.order.create(
            {
                'receipt': receipt,
                'amount': amount,
                'currency': currency,
                'payment_capture': '1',
            }
        )
        print(order)

        #==============================================================================================================================
        order1 = None
        try:
            existing_order = Addmoney.objects.get(user=user)
            existing_order.order_id = order['id']
            existing_order.amount = int(amount) / 100
            existing_order.save()
        except Addmoney.DoesNotExist:
            # Create a new order if the user doesn't exist
            order1 = Addmoney(
                user=user,
                order_id=order['id'],
                amount=int(amount) / 100,
            )
            order1.save()



        #================================================================================================================================
        context = {
            'name': user,
            'order': order,
            'orderid': order['id'],
        }
        return render(request, 'payment.html', context)

@csrf_exempt
def razorpayhandler(request):
    if request.method == 'POST':
        data = request.POST
        famt = None
        print(data)
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        payment = Addmoney.objects.latest('order_id')
        print(payment)

        #wallet_payment
        lamt = payment.amount
        famt = payment.final_amount
        if razorpay_order_id == payment.order_id:
            payment.payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.final_amount = famt + lamt
            payment.status = True
            payment.save()

            user = request.user.id
            try:
                ewallet = Addmoney.objects.get(user=user)
                balance = ewallet.final_amount
            except Addmoney.DoesNotExist:
                # Handle the case where the user's EWallet does not exist
                balance = 0.00

            context = {
                'data': data,
                'balance': balance,
            }

            return redirect('estimate')
        else:
            return redirect('addmoney')


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def my_wallet(request):
    wallet = request.user.wallet
    return render(request, 'my_wallet.html', {'wallet': wallet})


def send_otp(mobile, otp, request):
    print("FUNCTION CALLED")
    conn = http.client.HTTPSConnection("www.smsgateway.center")

    # Send SMS OTP message
    msg = 'EVC Global App Login OTP is ' + otp + \
          '. OTP is valid for 5 minutes. Do not share this with anyone for security reason.'
    url = 'https://www.smsgateway.center/SMSApi/rest/send'
    payload = {
        'userId': 'evcglobal',
        'password': 'Evcglob@l2022',
        'senderId': 'EVCGLO',
        'sendMethod': 'simpleMsg',
        'msgType': 'text',
        'mobile': f'91{mobile}',
        'msg': msg,
        'duplicateCheck': 'true',
        'format': 'json'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'Cookie_1=value; Cookie_2=value'
    }
    response = requests.post(url, headers=headers, data=payload)
    print(response)
    return None


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')

        try:
            user = User.objects.create_user(username=email, email=email, first_name=name)
            user.save()
        except IntegrityError:
            context = {'message': 'User already exists', 'class': 'danger'}
            return render(request, 'register.html', context)

        otp = str(random.randint(1000, 9999))
        profile = Profile(user=user, mobile=mobile, otp=otp)
        profile.save()

        send_otp(mobile, otp, request)
        request.session['mobile'] = mobile

        return redirect('otp')

    return render(request, 'register.html')


def otp(request):
    mobile = request.session['mobile']
    context = {'mobile': mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        print(f'otp: {profile.otp}')

        if otp == profile.otp:
            return redirect('estimate')
        else:
            print('Wrong')

            context = {'message': 'Wrong OTP', 'class': 'danger', 'mobile': mobile}
            return render(request, 'otp.html', context)

    return render(request, 'otp.html', context)

def verify_otp(request):
    mobile = request.session['mobile']
    context = {'mobile': mobile}

    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()
        print(f'otp: {profile.otp}')
        if otp == profile.otp:
            user = profile.user
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # Set the backend attribute
            login(request, user)
            return redirect('estimate')
        else:
            context = {'message': 'Wrong OTP', 'class': 'danger', 'mobile': mobile}
            return render(request, 'verify_otp.html', context)

    return render(request, 'verify_otp.html', context)


def user_login(request):

    #24/09/2023
    global charger_id_group
    charger_id_group = request.GET.get('charger_id_group')
    print("charger id: ", charger_id_group)



    if request.method == 'POST':
        mobile = request.POST.get('mobile')

        user = Profile.objects.filter(mobile=mobile).first()

        if user is None:
            context = {'message1': 'User not found', 'class': 'danger'}
            return render(request, 'login.html', context)

        otp = str(random.randint(1000, 9999))
        user.otp = otp
        user.save()
        send_otp(mobile, otp, request)
        request.session['mobile'] = mobile
        return redirect('verify_otp')
    return render(request, 'login.html')


def get_payload(request, callm_id):
    callm = Callm.objects.get(id=callm_id)
    payload = callm.payload
    return JsonResponse({'payload': payload})



from django.http import JsonResponse
from ocpp_lib.call import Call
from ocpp_lib.types import *
from datetime import datetime, timedelta





async def trigger_remote_start_transaction(request):
    try:
        global charger_id_group
        global input_value
        time = (input_value / 12.5) * 60
        response = await Call.CallHandler.issue_command(
            charger_id=charger_id_group,
            request=RemoteStartTransaction_Req(
                idTag=IdToken(
                    IdToken="",
                ),
                connectorId=1,
            ),
        )
        return redirect('stop')

    except Exception as e:
        print(f"An error occurred: {e}")
        return redirect('error')




async def trigger_remote_stop_transaction(request):
    global charger_id_group
    response = await Call.CallHandler.issue_command(
    charger_id=charger_id_group,
    request=RemoteStopTransaction_Req(
        transactionId=1
    ),
    )
    return redirect('billinfo')

@login_required
def stop(request):
    first_charging_station = ChargingStations.objects.latest('id')
    change_amount = first_charging_station.Cost_per_Unit


    #StatusNotification Check start
    global chrg_amt
    most_recent_status_notification = Callm.objects.filter(action="StatusNotification").order_by('-sent_at').first()

    charger_payload_str = most_recent_status_notification.payload
    charger_message_dict = eval(charger_payload_str)
    charger_message = charger_message_dict['timestamp']
    charger_message_Status = charger_message_dict['status']
    print(most_recent_status_notification)
    charger_timestamp = datetime.strptime(charger_message, "%Y-%m-%dT%H:%M:%S.%fZ")
    print(charger_timestamp)
    current_time = datetime.utcnow()
    time_difference = current_time - charger_timestamp
    print(current_time)

    if time_difference <= timedelta(minutes=15) and charger_message_Status == 'Preparing':
        global chrg_amt
        time = round((((chrg_amt/12.5)*60)*1000), 2)

        context = {
            'time': time,
            'change_amount':change_amount,
        }
        return render(request, 'stop.html', context)
    else:
        context = {'message': 'Please Connect the Charger Plug', 'class': 'danger'}
        return render(request, 'start.html', context)

    #StatusNotification Check end

    # global chrg_amt
    # time = round((((chrg_amt/12.5)*60)*1000), 2)

    # context = {
    #     'time': time,
    # }
    # return render(request, 'stop.html', context)

#===============================================================END========================================================================



#dashboard

def station(request):
    try:
        if request.method == 'POST':
            station_name = request.POST['station_name']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            zip_code = request.POST['zip']
            station_type = request.POST['Public']
            open_24_7 = request.POST['Yes']
            phone = request.POST['phone']
            print(station_name,address,city,state,zip_code,station_type,open_24_7,phone)

            charging_station = ChargingStations(
                Charging_Station_Name=station_name,
                Address=address,
                City=city,
                State=state,
                Zip_Code=zip_code,
                station_type=station_type,
                open=open_24_7,
                Phone_Number=phone
            )
            charging_station.save()

            return render(request, 'station.html')
    except Exception as e:
        print(str(e))
    charging_stations = ChargingStations.objects.all()
    return render(request, 'station.html', {'charging_stations': charging_stations})


def logs(request):
    callm_objects = Callm.objects.order_by('-id')[:500]
    return render(request, 'logs.html', {'callm_objects': callm_objects})


def logindash(request):
    if request.method == 'POST':
        #input field
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        print (username , pass1)
        if username == "admin" and pass1 == "admin":
            return render (request , 'dashboard.html')
        else:
            return render(request , 'logindash.html')
 
    return render(request, 'logindash.html')
 
 
 
def dashboard(request):
    # Perform the query to get the total counts
    result = ChargingStations.objects.aggregate(
        total_charging_points=Sum('Socket_URL'),
        total_connectors=Sum('Connectors')
    )
    # Access the total counts from the result
    total_charging_points = result['total_charging_points']
    total_connectors = result['total_connectors']
 
    # Pass the counts to the template context




    charging_stations = ChargingStations.objects.all()
    for charging_station in charging_stations:
        number_point = charging_station.Charging_Point_Name
    print(number_point)

    context = {
        'charging_station_count': ChargingStations.objects.count(),
        'total_charging_points': total_charging_points,
        'total_connectors': total_connectors,
        'number_point':number_point,
    }
 
    return render(request, 'dashboard.html', context)

 
def newstation(request):
    reviews = Review.objects.all().order_by('-id')
    count = Review.objects.count()


    callm_objects = Callm.objects.order_by('-id')[:500]



    if request.method == 'POST':
        #general
        Charging_Station_Name = request.POST.get('station_name')
        Address = request.POST.get('address')
        City = request.POST.get('city')
        Zip = request.POST.get('zip')
        State = request.POST.get('state')
        Country = request.POST.get('country')
        Station_type = request.POST.getlist('staiontypre')
        openhr = request.POST.getlist('openn')
        Phone = request.POST.get('phone')

        #charging points
        Socket_URL = request.POST.get('socket_url')
        Charging_Point_Name = request.POST.get('point_name')
        Charging_Point_ID = request.POST.get('point_id')
        Connector_Type = request.POST.get('connector_type')
        Charging_Power = request.POST.get('charging_power')
        EV_Compatible = request.POST.get('vehicle_type')
        Cost_per_Unit = request.POST.get('price')
        LICENSE = request.POST.get('license')
        Change_Availability = request.POST.get('change_availability')
        

        #amenity
        food_drink = request.POST.getlist('food_drink')
        Things_to_Do = request.POST.getlist('Things_to_Do')
        Shopping = request.POST.getlist('Shopping')
        Services = request.POST.getlist('Services')

        #saving in databse
        charging_station = ChargingStations(
            #general
            Charging_Station_Name=Charging_Station_Name,
            Address=Address,
            City=City,
            Zip_Code=Zip,
            State=State,
            Country=Country,
            station_type=Station_type,
            open=openhr,
            Phone_Number=Phone,

            #charging point
            Socket_URL=Socket_URL,
            Charging_Point_Name=Charging_Point_Name,
            Charging_Point_ID=Charging_Point_ID,
            Connector_Type=Connector_Type,
            Charging_Power=Charging_Power,
            EV_Compatible=EV_Compatible,
            Cost_per_Unit=Cost_per_Unit,
            LICENSE=LICENSE,
            Change_Availability=Change_Availability,

            #amenities

            Food_Drink=food_drink,
            Things_to_Do=Things_to_Do,
            Shopping=Shopping,
            Services=Services,
            )
        charging_station.save()
        
        print(Charging_Station_Name,Services)

    return render(request, 'newstation.html',{'reviews':reviews, 'count':count, 'callm_objects': callm_objects})
 
def rfid(request):
    return render(request, 'rfid.html')
 
def role(request):
    return render(request, 'role.html')
 
def user(request):
    return render(request, 'user.html')


def delete(request, id):
    mem  =  ChargingStations.objects.get(id=id)
    mem.delete()
    return redirect('station')


def edit(request, id):
    mem  =  ChargingStations.objects.get(id=id)
    callm_objects = Callm.objects.order_by('-id')[:500]
    reviews = Review.objects.all().order_by('-id')
    print(mem.City)
    return render(request, 'edit.html', {'mem': mem, 'callm_objects': callm_objects, 'reviews':reviews})

def update(request, id):
        
    #general
    Charging_Station_Name = request.POST.get('station_name')
    Address = request.POST.get('address')
    City = request.POST.get('city')
    Zip = request.POST.get('zip')
    State = request.POST.get('state')
    Country = request.POST.get('country')
    Station_type = request.POST.getlist('staiontypre')
    openhr = request.POST.getlist('openn')
    Phone = request.POST.get('phone')

    #charging points
    Socket_URL = request.POST.get('socket_url')
    Charging_Point_Name = request.POST.get('point_name')
    Charging_Point_ID = request.POST.get('point_id')
    Connector_Type = request.POST.get('connector_type')
    Charging_Power = request.POST.get('charging_power')
    EV_Compatible = request.POST.get('vehicle_type')
    Cost_per_Unit = request.POST.get('price')
    LICENSE = request.POST.get('license')
    Change_Availability = request.POST.get('change_availability')

    #amenity
    food_drink = request.POST.getlist('food_drink')
    Things_to_Do = request.POST.getlist('Things_to_Do')
    Shopping = request.POST.getlist('Shopping')
    Services = request.POST.getlist('Services')



    member = ChargingStations.objects.get(id=id)
    #general
    member.Charging_Station_Name = Charging_Station_Name
    member.Address = Address
    member.City = City
    member.Zip_Code = Zip
    member.State = State
    member.Country = Country
    member.station_type = Station_type
    member.open = openhr
    member.Phone_Number = Phone
    #charging point
    member.Socket_URL = Socket_URL
    member.Charging_Point_Name = Charging_Point_Name
    member.Charging_Point_ID = Charging_Point_ID
    member.Connector_Type = Connector_Type
    member.Charging_Power = Charging_Power
    member.EV_Compatible = EV_Compatible
    member.Cost_per_Unit = Cost_per_Unit
    member.LICENSE = LICENSE
    member.Change_Availability = Change_Availability
    #amenities
    member.Food_Drink = food_drink
    member.Things_to_Do = Things_to_Do
    member.Shopping = Shopping
    member.Services = Services
    member.save()
    return redirect('station')


#conditions
def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')

def refund(request):
    return render(request, 'refund.html')





















#15/08/2023
async def API_START(request):
    response = await Call.CallHandler.issue_command(
    charger_id="EVCMUM00001",
    request=RemoteStartTransaction_Req(
        idTag=IdToken(
            IdToken="",
        ),
        connectorId=1,
    ),)
    return HttpResponse('success', "Start transaction")



async def API_STOP(request):
    response = await Call.CallHandler.issue_command(
    charger_id="EVCMUM00001",
    request=RemoteStopTransaction_Req(
        transactionId=1
    ),
    )
    return HttpResponse('success', "Stop transaction")














#meter:
# {'connectorId': 1, 'meterValue': [{'sampledValue': [{'context': 'Sample.Periodic', 'format': 'Raw', 'location': 'Outlet', 'measurand': 'Energy.Active.Import.Register', 'unit': 'Wh', 'value': '5000'}], 'timestamp': '2023-06-06T12:27:22.872Z'}, {'sampledValue': [{'context': 'Sample.Clock', 'format': 'Raw', 'location': 'EV', 'measurand': 'SoC', 'unit': 'Percent', 'value': '62'}], 'timestamp': '2023-06-06T12:27:22.872Z'}, {'sampledValue': [{'context': 'Sample.Clock', 'format': 'Raw', 'location': 'Outlet', 'measurand': 'Voltage', 'unit': 'V', 'value': '347.0'}], 'timestamp': '2023-06-06T12:27:22.873Z'}, {'sampledValue': [{'context': 'Sample.Clock', 'format': 'Raw', 'location': 'Outlet', 'measurand': 'Current.Import', 'unit': 'A', 'value': '61.10'}], 'timestamp': '2023-06-06T12:27:22.874Z'}, {'sampledValue': [{'context': 'Sample.Clock', 'format': 'Raw', 'location': 'Body', 'measurand': 'Temperature', 'unit': 'Celsius', 'value': '44.3'}], 'timestamp': '2023-06-06T12:27:22.875Z'}], 'transactionId': 1227}