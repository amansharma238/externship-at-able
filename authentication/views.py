from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

# from django.core.paginator import Paginator
from .forms import MyUserCreationForm
from .models import Lead, Remark, SalesUser
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
            user = SalesUser.objects.get(username=email)
        except:
            messages.error(request, "User does not exist.")

        user = authenticate(request, username=email, password=password)

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
    return render(request, "login_register.html", context)


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

    return render(request, "login_register.html", {"form": form})


def home(request):
    context = {}
    return render(request, "home.html")


def analytics(request):
    return render(request, "analytics.html", {})


def remarkLead(request):
    # if request.method == "POST":
    #     mark = Remark.objects.get(user=request.user)
    #     message = Remark.objects.create(
    #         user=request.user, lead=mark.lead, remark=request.POST.get("remark")
    #     )
    context = {}
    return render(request, "remark.html", context)


# Sales representative will call the person and add remarks/view previous remarks
# Sales representative will mark the lead as hot/cold/med etc
# Commit Message: Adding Notes Implemented
# Note: While implementing sales represenative use Ajax as we do not want page to reload after submitting the remarks.
