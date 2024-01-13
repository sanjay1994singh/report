from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render


@login_required(login_url='/accounts/login-user/')
# Create your views here.
def homepage(request):
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
