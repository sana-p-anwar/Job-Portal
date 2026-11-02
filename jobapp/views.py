from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from jobapp.models import JobDB
from jobapp.serializers import JobSerializer
from jobapp.models import ApplicationDb
from jobapp.serializers import ApplicationSerializer


# Create your views here.

class JobListCreateView(APIView):

    def get(self, request):

        qs = JobDB.objects.all()

        serializer_instance = JobSerializer(qs, many=True)

        return Response(data=serializer_instance.data)

    def post(self, request):

        form_data = request.data

        serializer_instance = JobSerializer(data=form_data)

        if serializer_instance.is_valid():

            actual_data = serializer_instance.validated_data

            JobDB.objects.create(**actual_data)

            return Response(data={
                "message": "Job added successfully."
            })

        else:

            return Response(data={
                "errors": serializer_instance.errors
            })
class JobRetrieveUpdateDeleteView(APIView):
    
    def get(self, request, pk):

        qs = JobDB.objects.get(id=pk)

        serializer_instance = JobSerializer(qs)

        return Response(data=serializer_instance.data)

    def put(self, request, pk):

        form_data = request.data

        serializer_instance = JobSerializer(data=form_data)

        if serializer_instance.is_valid():

            actual_data = serializer_instance.validated_data

            JobDB.objects.filter(id=pk).update(**actual_data)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

    def delete(self, request, pk):

        JobDB.objects.filter(id=pk).delete()

        return Response({
            "Message": "Job deleted successfully..!"
        })
class ApplicationListCreateView(APIView):
    
    def get(self, request):

        qs = ApplicationDb.objects.all()

        application_instance = ApplicationSerializer(qs, many=True)

        return Response(data=application_instance.data)

    def post(self, request):

        form_data = request.data

        serializer_instance = ApplicationSerializer(data=form_data)

        if serializer_instance.is_valid():

            actual_data = serializer_instance.validated_data

            ApplicationDb.objects.create(**actual_data)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)
        
class ApplicationRetrieveUpdateDeleteView(APIView):
    
    def get(self, request, pk):

        # Retrieve application using ID
        qs = get_object_or_404(ApplicationDb, id=pk)

        application_instance = ApplicationSerializer(qs)

        return Response(data=application_instance.data)
class EvaluateApplicationView(APIView):
    
    def put(self, request, pk):

        form_data = request.data

        ApplicationDb.objects.filter(id=pk).update(**form_data)

        return Response(data={
            "Message": "Application status updated..!"
        })