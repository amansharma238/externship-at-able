# from django.contrib.auth.models import User
from multiprocessing import context
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import MyUserCreationForm
from .models import Lead, SalesUser
from django.contrib import messages
# Create your views here.


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = SalesUser.objects.get(username=email)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            user2 = SalesUser.objects.filter(
                username=email).values('is_approved')
            print(user2[0]['is_approved'])
            if user2[0]['is_approved']:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(
                    request, 'You are not yet approved!!, contact to website admin')
        else:
            messages.error(request, 'Username or Password does not exist.')

    context = {'page': page}
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.save()
            messages.success(
                request, 'Thanks For registration!!, Login After few hours')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'login_register.html', {'form': form})


def home(request):
    leads = Lead.objects.all()
    context = {'leads': leads}
    return render(request, 'home.html', context)
