from api.serializers import ProjectSerializer
from projects.models import Project, Review
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET':'/api/v1/projects'},
        {'GET':'/api/v1/projects/id'},
        {'POST':'/api/v1/projects/id/votes'},
        
        {'POST':'/api/v1/users/token'},
        {'POST':'/api/v1/userss/token/refresh'},
    ]

    return Response(routes)

#get all projects
@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)

    return Response(serializer.data)

#get a single project
@api_view(['GET'])
def getSingleProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    review, created = Review.objects.get_or_create(
        owner=user,
        project=project
    )

    review.value = data['value']
    review.save()
    project.getVoteCount

    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)