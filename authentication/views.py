from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm
from .models import SalesUser
from django.contrib import messages

# Create your views here.


def error_404_view(request, exception):
    return render(request, "error.html")


def loginUser(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = SalesUser.objects.get(email=email)
        except:
            messages.error(request, "User does not exist.")

        user = authenticate(request, email=email, password=password)
        print("user", user)
        if user is not None:
            user2 = SalesUser.objects.filter(email=email).values("is_approved")
            # print(user2)
            if user2[0]["is_approved"]:
                login(request, user)
                return redirect("home")
            else:
                messages.warning(
                    request, "You are not yet approved!!, contact to website admin"
                )
        else:
            messages.error(request, "Username or Password does not exist.")

    context = {"page": page}
    return render(request, "login.html", context)


@login_required
def logoutUser(request):
    logout(request)
    return redirect("home")


def registerUser(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.save()
            messages.success(
                request, "Thanks For registration!!, Login After few hours"
            )
        else:
            messages.error(request, "An error occured during registration")

    return render(request, "register.html", {"form": form})


def home(request):
    page = "login"
    if request.user.is_authenticated:
        return render(request, "home.html")
    return render(request, "login.html", {"page": page})


@login_required
def analytics(request):
    return render(request, "analytics.html", {})
