from rest_framework import serializers
from jobapp.models import JobDB
from jobapp.models import ApplicationDb



class JobSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)

    title = serializers.CharField(max_length=200)

    company_name = serializers.CharField(max_length=200)

    location = serializers.CharField(max_length=200)

    job_type = serializers.ChoiceField(
        choices=JobDB.JOB_TYPE_CHOICES,
        default="full_time"
    )

    experience = serializers.CharField(max_length=100)

    salary = serializers.CharField(max_length=100)

    description = serializers.CharField(max_length=1000)

    requirements = serializers.CharField(max_length=1000)

    published_date = serializers.DateTimeField(read_only=True)

    is_active = serializers.BooleanField(default=True)

class ApplicationSerializer(serializers.Serializer):
    
    id = serializers.IntegerField(read_only=True)

    job_id = serializers.IntegerField()

    applicant_name = serializers.CharField(max_length=100)

    email = serializers.EmailField()

    cover_letter = serializers.CharField()

    resume_link = serializers.URLField()

    status = serializers.CharField(read_only=True)

    application_date = serializers.DateTimeField(read_only=True)

    def validate(self, validate_data):

        job_id = validate_data.get("job_id")

        if not JobDB.objects.filter(id=job_id).exists():

            raise serializers.ValidationError("Job does not exist...!")

        return validate_data    