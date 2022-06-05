from users.models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def profilesPagination(request, profiles, results):

    #pagination config
    page = request.GET.get('page')
    
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex= (int(page) - 4)
    rightIndex= (int(page) + 5)

    if leftIndex < 1:
        leftIndex = 1
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles

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