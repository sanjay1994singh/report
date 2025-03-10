import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from purchased_service.models import ServicePurchased
from services.models import ServiceMaster, ServicePrice
from datetime import datetime, timedelta

from accounts.models import CustomUser


def homepage(request):
    if request.method == 'POST':
        form = request.POST
        full_name = form.get('full_name')
        email = form.get('email')
        mobile = form.get('mobile')
        password = form.get('password')
        user = CustomUser.objects.create_user(full_name=full_name,
                                              username=mobile,
                                              email=email,
                                              mobile=mobile,
                                              password=password,
                                              )
        if user:
            status = 'success'
            msg = 'Registration successfully.'
        else:
            status = 'failed!'
            msg = 'Registration failed?'

        context = {
            'status': status,
            'msg': msg,
        }
        return JsonResponse(context)
    else:
        return render(request, 'create_report.html')


# @login_required(login_url='/accounts/login-user/')
def my_service(request):
    user_id = request.session.get('user_id')
    purchased_service = ServicePurchased.objects.filter(user_id=user_id, payment_status='success')
    service = purchased_service
    return render(request, 'my_service.html', {'service': service})


@login_required(login_url='/accounts/login-user/')
def get_services(request):
    service = ServiceMaster.objects.all()
    service_list = []
    for i in service:
        service_dict = {}
        service_dict['id'] = i.id
        service_dict['name'] = i.name
        service_dict['desc'] = i.desc
        service_dict['img'] = i.img.url
        service_list.append(service_dict)
    context = {
        'service': service_list,
    }
    return JsonResponse(context)


@login_required(login_url='/accounts/login-user/')
def get_my_services(request):
    service = ServiceMaster.objects.all()
    service_list = []
    for i in service:
        service_price = ServicePrice.objects.filter(service_id=i.id)
        if service_price:
            price = service_price[0].price
        else:
            price = 'Free'
        service_dict = {}
        service_dict['id'] = i.id
        service_dict['name'] = i.name
        service_dict['desc'] = i.desc
        service_dict['img'] = i.img.url
        service_dict['price'] = price
        service_list.append(service_dict)
    context = {
        'service': service_list,
    }
    return JsonResponse(context)


@login_required(login_url='/accounts/login-user/')
def buy_service_detail(request, service_id):
    service_data = ServiceMaster.objects.get(id=service_id)
    context = {
        'service_data': service_data
    }
    return render(request, 'buy_service_detail.html', context)


@login_required(login_url='/accounts/login-user/')
def get_service_month(request):
    if request.method == 'GET':
        form = request.GET
        service_id = form.get('service_id')
        price_data = ServicePrice.objects.filter(service_id=service_id)
        data_list = []
        if price_data:
            for i in price_data:
                data_dict = {}
                data_dict['id'] = i.id
                data_dict['month'] = i.month
                data_dict['price'] = i.price
                data_list.append(data_dict)

        context = {
            'data': data_list
        }
        return JsonResponse(context)


@login_required(login_url='/accounts/login-user/')
def get_service_price(request):
    if request.method == 'GET':
        form = request.GET
        user_id = request.session.get('user_id')
        service_id = form.get('service_id')
        month_id = form.get('month_id')

        data_dict = {}
        price_data = ServicePrice.objects.get(id=month_id)
        data_dict['month'] = price_data.month
        data_dict['price'] = price_data.price

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment = client.order.create(
            {'amount': int(data_dict['price']) * 100, 'currency': 'INR', 'payment_capture': '1'})
        order_id = payment['id']

        same_user = ServicePurchased.objects.filter(user_id=user_id, service_id=service_id)
        if same_user:
            ServicePurchased.objects.filter(user_id=user_id).update(razorpay_order_id=order_id)
        else:
            ServicePurchased.objects.create(user_id=user_id, razorpay_order_id=order_id, service_id=service_id)
        context = {
            'data': data_dict,
            'payment': payment,
            'order_id': order_id,
        }
        return JsonResponse(context)



def create_article(request):
    if request.method == 'POST':
        form = request.POST
        title = form.get('Title')
        city = form.get('City')
        channel = form.get('channel')
        reporter = form.get('reporter')
        description = form.get('Description')
        file = form.get('img_pre_iv')
        context = {
            'title': title,
            'city': city,
            'reporter': reporter,
            'channel': channel,
            'description': description,
            'file': file,
        }
        return JsonResponse(context)

    return render(request, 'create_report.html')


def download_report(request):
    if request.method == "POST":
        form = request.POST
        title = form.get('title', '')
        city = form.get('city', '')
        reporter = form.get('reporter', '')
        channel = form.get('channel', '')
        description = form.get('description', '')
        file = form.get('file', '')
        if reporter:
            reporter = str(reporter)
        else:
            reporter = ''
        context = {
            'title': title,
            'city': city,
            'description': description,
            'file': file,
            'reporter': reporter,
            'channel': channel,
        }
        return render(request, 'download_report.html', context)


def calculate_future_date(months):
    current_date = datetime.now()
    future_date = current_date + timedelta(days=30 * months)  # Assuming a month has 30 days for simplicity
    return future_date


def payment_success(request):
    if request.method == 'GET':
        form = request.GET
        user_id = request.session.get('user_id')
        razorpay_order_id = form.get('razorpay_order_id', None)
        razorpay_payment_id = form.get('razorpay_payment_id', None)
        razorpay_signature = form.get('razorpay_signature', None)
        service_id = form.get('service_id', None)
        price = form.get('price', None)
        discount = form.get('discount', None)
        totalprice = form.get('totalprice', None)
        quantity = form.get('quantity', None)
        payment_status = form.get('payment_status', None)
        months = int(form.get('month', 0))
        status = 0
        msg = 'Service not bought.'
        future_date = calculate_future_date(months)
        try:

            service_obj = ServicePurchased.objects.filter(user_id=user_id, razorpay_order_id=razorpay_order_id).update(
                service_id=service_id, price=price, discount=discount, total_price=totalprice, qty=quantity,
                razorpay_payment_id=razorpay_payment_id, razorpay_signature=razorpay_signature,
                payment_status=payment_status, end_date=future_date, month=months)
            if service_obj:
                status = 1
                msg = 'Service buy successfully.'

        except Exception as e:
            print(e, 'error in payment success function')
            msg = str(e)
        context = {
            'status': status,
            'msg': msg
        }
        return JsonResponse(context)
