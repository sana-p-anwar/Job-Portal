
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, serializers

from jobapp.models import JobDB, ApplicationDb
from jobapp.serializers import JobSerializer, ApplicationSerializer, UserSerializer


# Create your views here.

class SignUpView(APIView):

    def post(self, request):

        form_data = request.data

        serializer_instance = UserSerializer(data=form_data)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(
                data=serializer_instance.data,
                status=201
            )

        else:
            return Response(
                serializer_instance.errors,
                status=400
            )

    def get(self, request):

        qs = User.objects.all()

        serializer = UserSerializer(qs, many=True)

        return Response(serializer.data)


class UserListDeleteView(APIView):

    def delete(self, request):

        user_id = request.data.get('id')

        user = User.objects.get(id=user_id)

        user.delete()

        return Response({
            "Message": "User deleted successfully"
        }, status=200)


class JobListCreateView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        qs = JobDB.objects.filter(created_by=request.user)

        serializer_instance = JobSerializer(qs, many=True)

        return Response(data=serializer_instance.data)

    def post(self, request):

        form_data = request.data

        serializer_instance = JobSerializer(data=form_data)

        if serializer_instance.is_valid():

            serializer_instance.save(created_by=request.user)

            return Response(data={
                "Message": "Job Created Successfully..!",
                "Your Job Details": serializer_instance.data
            })

        else:
            return Response(data=serializer_instance.errors)


class JobRetrieveUpdateDeleteView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):

        job_object = get_object_or_404(JobDB, id=pk)

        if job_object.created_by == request.user:

            serializer_instance = JobSerializer(job_object)

            return Response(data=serializer_instance.data)

        else:
            raise serializers.ValidationError("Access Denied..!")

    def put(self, request, pk):

        job_object = get_object_or_404(JobDB, id=pk)

        if job_object.created_by != request.user:

            raise serializers.ValidationError("Access Denied..!")

        form_data = request.data

        serializer_instance = JobSerializer(
            data=form_data,
            instance=job_object
        )

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data={
                "message": "Job details updated successfully",
                "updated data": serializer_instance.data
            })

        else:
            return Response(data=serializer_instance.errors)

    def delete(self, request, pk):

        job_object = get_object_or_404(JobDB, id=pk)

        if job_object.created_by != request.user:

            raise serializers.ValidationError("Access Denied..!")

        job_object.delete()

        return Response(data={
            "message": "Job deleted successfully..!"
        })


# Keep your existing Application views below this point.


class ApplicationListCreateView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = ApplicationDb.objects.filter(applicant=request.user)
        application_instance = ApplicationSerializer(qs, many=True)
        return Response(data=application_instance.data)

    def post(self, request):
        form_data = request.data

        serializer_instance = ApplicationSerializer(
            data=form_data,
            context={"request": request}
        )

        if serializer_instance.is_valid():
            serializer_instance.save(applicant=request.user)

            return Response(data={
                "Message": "Application submitted successfully..!",
                "Application Details": serializer_instance.data
            })

        else:
            return Response(data=serializer_instance.errors)

        
        
class ApplicationRetrieveUpdateDeleteView(APIView):
    
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):

        application_object = get_object_or_404(
            ApplicationDb,
            id=pk,
            applicant=request.user
        )

        application_object.delete()

        return Response(data={
            "Message": "Application withdrawn successfully..!"
        })

class EvaluateApplicationView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):

        application_object = get_object_or_404(ApplicationDb, id=pk)

        # Check whether the logged-in user created this job
        if application_object.job.created_by != request.user:
            return Response(data={
                "Message": "You are not authorized to update this application status..!"
            }, status=403)

        # Update only status
        status = request.data.get("status")

        if status not in ["applied", "under_review", "shortlisted", "rejected", "selected"]:
            return Response(data={
                "Message": "Invalid application status..!"
            }, status=400)

        application_object.status = status
        application_object.save()

        return Response(data={
            "Message": "Application status updated successfully..!"
        })
