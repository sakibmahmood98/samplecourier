from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Register, Orders
import random


def index(request):
    return render(request, "index.html")



def login(request):
    if request.method == 'POST':
        try:
            data = Register.objects.get(phone = request.POST['phone'])
        except:
            return render(request, "login.html", {"invalid_cred": 'Invalid Credentials'}) 
        
        if str(data.password) == str(request.POST['password']):
            request.session['name'] = data.name
            request.session['phone'] = data.phone
            print(request.session['phone'])
            request.session['usertype'] = data.usertype
            print(data.name)

            if str(data.usertype) == 'Admin':    ##ADMIN or MARCHANT
                return redirect("/cdash", {"username": request.session['name']})
            else:
                return redirect("/ddash", {"username": request.session['name']})
        else:

            return render(request, "login.html", {"invalid_cred": 'Invalid Credentials'})    
    else:
        return render(request, "login.html")



def logout(request):
    request.session.flush()
    return redirect("/login")



def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone'].replace(" ","")
        password1 = request.POST['password1'].replace(" ","")
        password2 = request.POST['password2'].replace(" ","")
        usertype = request.POST['usertype'].replace(" ","")
        email = request.POST['email'].replace(" ","")
        address = request.POST['address']

        register = Register()

        if str(password1) == str(password2):
            register.name = name
            register.phone = phone
            register.password = password1
            register.usertype = usertype
            register.email = email
            register.address = address
            register.save()

            return redirect("/login")
        else:
            return redirect("/signup")

    return render(request, "signup.html")



def ddash(request):
    try:
        order = Orders.objects.get(marchant_phone = request.session['phone'])
        orders = Orders.objects.filter(order_status = 'placed')
        return render(request, "ddash.html", {"orders": orders})
    except:
        orders = Orders.objects.filter(order_status = 'placed')
        return render(request, "ddash.html", {"orders": orders})





def cdash(request):
    if request.method == 'POST' and 'cost_cal' in request.POST:

        weight = request.POST['weight'].replace(" ","")


        parcel_product_type = request.POST['parcel_product_type'].replace(" ","")
        parcel_dest_choice = request.POST['parcel_dest_choice'].replace(" ", "")
        parcel_dest = request.POST['parcel_dest'].replace(" ", "")

        if int(weight) == 2 and str(parcel_dest_choice) == 'DH' : base_price = 60
        elif int(weight) == 3 and str(parcel_dest_choice) == 'DH' : base_price = 70
        elif int(weight) == 4 and str(parcel_dest_choice) == 'DH' : base_price = 80
        elif int(weight) == 5 and str(parcel_dest_choice) == 'DH' : base_price = 90
        elif int(weight) == 2 and str(parcel_dest_choice) == 'DD' : base_price = 110
        elif int(weight) == 3 and str(parcel_dest_choice) == 'DD' : base_price = 130
        elif int(weight) == 4 and str(parcel_dest_choice) == 'DD' : base_price = 150
        elif int(weight) == 5 and str(parcel_dest_choice) == 'DD' : base_price = 170
        elif int(weight) == 2 and str(parcel_dest_choice) == 'OD' : base_price = 130
        elif int(weight) == 3 and str(parcel_dest_choice) == 'OD' : base_price = 150
        elif int(weight) == 4 and str(parcel_dest_choice) == 'OD' : base_price = 170
        elif int(weight) == 5 and str(parcel_dest_choice) == 'OD' : base_price = 190

        if str(parcel_dest_choice) == 'DH': ans = base_price
        elif str(parcel_dest_choice) == 'NN' : ans = 0
        else : ans = base_price + ((base_price*50) / 100) + ((base_price * 1) / 100)

        total_price = ans


        request.session['weight'] = weight

        request.session['total_price'] = total_price

        request.session['parcel_product_type'] = parcel_product_type
        request.session['parcel_dest_choice'] = parcel_dest_choice
        request.session['parcel_dest'] = parcel_dest

        return render(request, "cdash.html", {"total_price": total_price})

    elif request.method == 'POST' and 'confirm' in request.POST:

        # rcvr_name = request.POST['rcvr_name']
        # rcvr_email = request.POST['rcvr_email']
        # rcvr_phone = request.POST['rcvr_phone']
        
        # pickup_address = request.POST['pickup_address']
        # deliver_address = request.POST['deliver_address']

        invoice_id = "ORD-N"+str(random.randint(0,9))+str(random.randint(0,9))
        orders = Orders()
        orders.invoice_id = invoice_id

        orders.parcel_weight = request.session['weight']

        orders.total_price = request.session['total_price']

        orders.parcel_product_type = request.session['parcel_product_type']
        orders.parcel_dest_choice = request.session['parcel_dest_choice']
        orders.parcel_dest = request.session['parcel_dest']

        orders.sender_name = request.session['name']
        orders.sender_phone = request.session['phone']

        orders.receiver_name = request.POST['rcvr_name']
        orders.receiver_phone = request.POST['rcvr_phone']

        orders.deliver_address = request.POST['deliver_address']
        orders.order_status = "placed"

        orders.save()

        return redirect("/order-history")
    
    else:
        try:
            order = Orders.objects.filter(sender_phone = request.session['phone']).order_by('id').last()
            print(order)

            return render(request, "cdash.html")
        except:
            return render(request, "cdash.html")


def order_history(request):
    orders = Orders.objects.filter(order_status = 'placed', sender_phone = request.session['phone'])
    return render(request, "order-history.html", {"orders": orders})