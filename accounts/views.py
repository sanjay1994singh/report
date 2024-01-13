from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from accounts.models import CustomUser


def login_user(request):
    if request.method == 'POST':
        form = request.POST
        mobile = form.get('Mobile')
        password = form.get('Password')

        mobile = mobile.strip()
        password = password.strip()
        user = CustomUser.objects.filter(username__iexact=mobile)
        if user:
            user = authenticate(username=mobile, password=password)
            login(request, user)
            request.session['user_id'] = user.id
            status = 1
        else:
            status = 0

        context = {
            'status': status,
        }
        return JsonResponse(context)
    return render(request, 'login_account.html')


def signup_user(request):
    if request.method == 'POST':
        form = request.POST
        mobile = form.get('Mobile')
        password = form.get('Password')
        user_type = form.get('user_type')

        mobile = mobile.strip()
        password = password.strip()

        status = 0
        try:
            user = CustomUser.objects.create_user(username=mobile,
                                                  mobile=mobile,
                                                  password=password,
                                                  user_type=user_type,
                                                  )
            if user:
                status = 1
        except Exception as e:
            print(e)
        context = {
            'status': status,
        }
        return JsonResponse(context)
    return render(request, 'signup_account.html')


def logout_user(request):
    logout(request)
    return redirect('/')
