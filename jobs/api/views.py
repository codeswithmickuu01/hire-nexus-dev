from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from.serializers import JobSerializer,jobDetailSerializer,JobPostSerializer, JObApplicationSerializer,MyApplicationSerializer,viewApplicationSerializer,ApplicationSerializer,RecruiterJobSerializer
from jobs.models import Job, Application
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_list(request):
    job_res = Job.objects.all()
    serializer = JobSerializer(job_res,many=True)
    return Response(serializer.data)



@api_view(['GET'])
def job_detail(request,id):
    try:
        job = Job.objects.get(id=id)
    except Job.DoesNotExist:
        return Response({"error":"Job Not Found"},status=status.http_404_NOT_FOUND)
    serializer = jobDetailSerializer(job)
    return Response(serializer.data)


@api_view(['POST'])
def create_job_api(request):
    serializer = JobPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message":"Job Created Successfully.",
                "job":serializer.data
            },status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_job_api(request):
    if request.user.roles != 'student':
        return Response(
            {"error" : "only student can apply for jobs"},
            status = status.HTTP_403_FORBIDDEN
        )
    
    serializer = JObApplicationSerializer(data=request.data)

    if serializer.is_valid():
        job = serializer.validated_data['job']

        if Application.objects.filter(job=job,student=request.user).exists:
            return Response({'error': 'you have already applied to this job'},status=status.HTTP_400_BAD_REQUEST)
        
        Application.objects.create(
            job=job,
            student=request.user
        )

        return Response({"message" : "job applied successfully"},status=status.HTTP_201_CREATED)
    return Response (serializer.error,status=status.HTTP_400_BAD_REQUEST)


# view application 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_application_api(request):
    if request.user.roles != 'student':
        return Response(
            { "error":"Only student can view applications"},
            status=status.HTTP_403_FORBIDDEN

        )
    application = Application.object.filter(student=request.user)
    Serializer = MyApplicationSerializer(application,many=True)
    return Response(Serializer.data)

# view Application for a job API 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_application_recruiter_api(request,job_id):
    if request.user.roles != 'recruiter':
        return Response(
            { "error":"Only student can view applications"},
            status=status.HTTP_403_FORBIDDEN 
        )
    
    try:
        job = Job.objects.get(id=job_id,posted_by=request.user )
    except Job.DoesNotExist:
        return Response(
            {"error":"JOb not found "},
            status=status.HTTP_403_FORBIDDEN
        )
    


    try:
        job = Job.objects.get(id=job_id,posted_by=request.user )
    except Job.DoesNotExist:
        return Response(
            {"error":"JOb not found or invalid data entered"},
            status=status.HTTP_404_FORBIDDEN
        )
    
    application = Application.objects.filter(job=job)
    Serializer = viewApplicationSerializer(application,many=True)
    return Response(Serializer.data)



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])

def update_application_status_api(request,job_id):

    if request.user.roles !='recruiter':
        return Response(
            {"error":"Only recruiters are allowed to update status "},
            status=status.HTTP_403_FORBIDDEN 

        )
    
    try:
        application = Application.objects.select_related('job').get(
            id=application_id,
            jod_posted_by=request.user
        )
        

    except Application.DoesNotExist:
        return Response(
            {"error":"Application not found or not authorized"},
            status=status.HTTP_404_NOT_FOUND
        )
    

    serializer = Application(
        application,
        data=request.user,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message":"Application status updated",
                "status":serializer.data['status']
            }
        )
    
    return Response(serializer.errors,status=status.HTTP_404_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_posted_job_api(request):
    if request.user.roles != 'recruiter':
        return Response(
            {"error":"Only recruiter can view their posted jobd"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    job = (
        Job.objects.filter(posted_by=request.user).annotate(applicants_counts=Count('application')).order_by('-created_at')

    )

    serializer = RecruiterJobSerializer(job,many=True)
    return Response(serializer.data)