from rest_framework import serializers
from jobs.models import Job ,Application
from jobs.models import Job, Application



class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'



class jobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Job
        fields = '__all__'



class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['title','description','company','location','job_type','posted_by','salary','deadline']



class JObApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        field = '__all__'


class MyApplicationSerializer(serializers.ModelSerializer):
    job_title  = serializers.CharField(source ='job.title',read_only=True )    
    company = serializers.CharField(source ='job.company',read_only=True )


    class meta:
        model = Application
        fields = [
            'id',
            'job_title',
            'company',
            'status',
            'applied_at',
        ]


class viewApplicationSerializer(serializers.ModelSerializer):
    student_email = serializers.CharField(source ='job.title',read_only=True )
    student_name  = serializers.CharField(source ='job.title',read_only=True )  



    class Meta:
        model = Application
        fields = [
            'id',
            'student_name',
            'student_email',
            'status',
            'applied_at'
        ]

class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = ['status']

class RecruiterJobSerializer(serializers.ModelSerializer):
    applicant_count = serializers.IntegerField(read_only=True)

    class Meta:
        field = [
            'id',
            'title',
            'company',
            'location',
            'job_type',
            'created_at',
            'applicants_counts'
        ]
