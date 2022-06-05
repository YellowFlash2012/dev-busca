from users.models import Profile, Skill
from django.db.models import Q

def searchProfiles(request):
    search_query = ""

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    print('search', search_query)

    skills = Skill.objects.filter(name__iexact=search_query)

    #name__icontains means it's not case sensitive
    #distinct() to only get 1 instance of each result
    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) | Q(short_intro__icontains=search_query) | Q(skill__in=skills))

    return profiles, search_query