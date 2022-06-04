from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm

from users.models import Profile

# Create your views here.
def profiles(request):
    profiles = Profile.objects.all()
    context = {"profiles":profiles}
    return render(request, "users/profiles.html", context)

def userProfile(request, pk):


    profile = Profile.objects.get(id=pk)

    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description="")

    context = {"profile":profile, "top_skills":top_skills, "other_skills":other_skills}
    
    return render(request, "users/user-profile.html", context)

def register_auth(request):
    page = 'register'
    form = SignUpForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get("email")
        
            user = User.objects.get(email=email)

            if user:
                messages.error(request, "Sorry but this user already exists!")

                return redirect("login")

            form = SignUpForm(request.POST)    
            new_user = form.save(commit=False)
            new_user.username = new_user.username.lower()
            new_user.save()
                
            messages.success(request, "Sign up successful!")

            login(request, new_user)

            return redirect("profiles")

        else:
            messages.error(request, "Error during signup, please try again!")


    context = {"page":page, "form":form}
    return render(request, "users/auth.html", context)

def login_auth(request):
    page = 'login'
    #prevent auth'd user from accessing profiles
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "Invalid credentials!")
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {{user.name}}")
            return redirect("profiles")
        else:
            messages.error(request, "Invalid credentials, please try again!")
            
    return render(request, "users/auth.html")

def logout_auth(request):
    messages.success(request, "Bye for now, see you next time!")
    logout(request)

    return redirect("login")