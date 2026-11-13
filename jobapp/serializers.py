from rest_framework import serializers
from jobapp.models import JobDB
from jobapp.models import ApplicationDb
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class JobSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = JobDB
        fields = "__all__"
        read_only_fields = ["id", "published_date", "created_by"]



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

        # Check whether job exists
        try:
            job = JobDB.objects.get(id=job_id)
        except JobDB.DoesNotExist:
            raise serializers.ValidationError("Job does not exist...!")

        # Check whether job creator is applying
        applicant = self.context["request"].user

        if job.created_by == applicant:
            raise serializers.ValidationError(
                "You cannot apply for your own job...!"
            )

        # Check whether applicant already applied
        if ApplicationDb.objects.filter(job=job, applicant=applicant).exists():
            raise serializers.ValidationError(
                "You have already applied for this job...!"
            )

        return validate_data

    def create(self, validated_data):

        job_id = validated_data.pop("job_id")
        job = JobDB.objects.get(id=job_id)

        applicant = validated_data.pop("applicant")

        return ApplicationDb.objects.create(
            job=job,
            applicant=applicant,
            **validated_data
        )
