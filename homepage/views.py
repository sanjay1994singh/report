from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from services.models import ServiceMaster, ServicePrice


def homepage(request):
    return render(request, 'index.html')


def get_services(request):
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
def create_article(request):
    if request.method == 'POST':
        form = request.POST
        title = form.get('Title')
        city = form.get('City')
        reporter = form.get('Reporter')
        description = form.get('Description')
        file = form.get('img_pre_iv')
        context = {
            'title': title,
            'city': city,
            'reporter': reporter,
            'description': description,
            'file': file,
        }
        return JsonResponse(context)

    return render(request, 'create_report.html')


@login_required(login_url='/accounts/login-user/')
def download_report(request):
    title = request.GET.get('title', '')
    city = request.GET.get('city', '')
    reporter = request.GET.get('reporter', '')
    description = request.GET.get('description', '')
    file = request.GET.get('file', '')
    if reporter:
        reporter = 'रिपोर्ट : ' + str(reporter)
    else:
        reporter = ''
    context = {
        'title': title,
        'city': city,
        'description': description,
        'file': file,
        'reporter': reporter,
    }
    return render(request, 'download_report.html', context)
