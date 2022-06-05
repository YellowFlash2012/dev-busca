
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.utils import profilesPagination, searchProfiles
from .forms import ProfileForm, SignUpForm, SkillForm

from users.models import Profile, Skill
from django.db.models import Q

# Create your views here.
def profiles(request):
    profiles, search_query = searchProfiles(request)

    custom_range, profiles = profilesPagination(request, profiles, 9)

    context = {"profiles":profiles, 'search_query':search_query, 'custom_range':custom_range}
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
            messages.success(request, "Account successfully edited!")
            return redirect('account')
    context={"form":form}
    return render(request, "users/profile_form.html", context)

@login_required(login_url='login')
def addSkill(request):
    page = 'add-new-skill'
    profile = request.user.profile

    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()

            messages.success(request, "New skill successfully added!")
            return redirect('account')
    context = {'form':form, 'page':page}

    return render(request, "users/skill_form.html", context)

@login_required(login_url='login')
def updateSkill(request, pk):
    page = 'update-skill'
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        #isntance=skill to prefill the form with the data to update
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            
            form.save()
            messages.success(request, "Skill successfully updated!")
            return redirect('account')
    context = {'form':form, 'page':page}

    return render(request, "users/skill_form.html", context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill successfully deleted!")
        return redirect('account')

    context = {'object':skill}
    return render(request, "delete_template.html", context)

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