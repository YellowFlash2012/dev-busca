from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm, SignUpForm

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

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {"profile":profile, 'skills':skills, 'projects':projects}
    return render(request, "users/account.html", context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context={"form":form}
    return render(request, "users/profile_form.html", context)

def register_auth(request):
    page = 'register'
    form = SignUpForm()
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "Sign up successful!")

            login(request, user)
            return redirect('edit-account')

        else:
            messages.success(
                request, 'An error has occurred during registration')

        # if form.is_valid():
        #     email = form.cleaned_data.get("email")
        
        #     user = User.objects.get(email=email)

        #     if user:
        #         messages.error(request, "Sorry but this user already exists!")

        #         return redirect("login")

    context = {"page":page, "form":form}
    return render(request, "users/auth.html", context)

def login_auth(request):
    page = 'login'
    #prevent auth'd user from accessing profiles
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Invalid credentials!")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}")
            return redirect("profiles")
        else:
            messages.error(request, "Invalid credentials, please try again!")
            
    return render(request, "users/auth.html")

def logout_auth(request):
    messages.success(request, "Bye for now, see you next time!")
    logout(request)

    return redirect("login")