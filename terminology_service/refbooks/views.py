from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Refbook, RefbookVersion, RefbookElement
from .serializers import RefbookSerializer, RefbookElementSerializer


class RefbookListView(APIView):
    def get(self, request):
        date_str = request.query_params.get('date', None)
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            refbooks = Refbook.objects.filter(versions__start_date__lte=date).distinct()
        else:
            refbooks = Refbook.objects.all()
        serializer = RefbookSerializer(refbooks, many=True)
        return Response({'refbooks': serializer.data}, status=status.HTTP_200_OK)


class RefbookElementListView(APIView):
    def get(self, request, id):
        version_str = request.query_params.get('version', None)
        refbook = get_object_or_404(Refbook, pk=id)
        if version_str:
            version = get_object_or_404(RefbookVersion, refbook=refbook, version=version_str)
        else:
            today = datetime.today().date()
            version = RefbookVersion.objects.filter(refbook=refbook, start_date__lte=today).order_by(
                '-start_date').first()

        if not version:
            return Response({'elements': []}, status=status.HTTP_200_OK)

        elements = RefbookElement.objects.filter(version=version)
        serializer = RefbookElementSerializer(elements, many=True)
        return Response({'elements': serializer.data}, status=status.HTTP_200_OK)


class CheckElementView(APIView):
    def get(self, request, id):
        code = request.query_params.get('code')
        value = request.query_params.get('value')
        version_str = request.query_params.get('version', None)
        refbook = get_object_or_404(Refbook, pk=id)

        if not code or not value:
            return Response({'error': 'Code and value parameters are required'}, status=status.HTTP_400_BAD_REQUEST)

        if version_str:
            version = get_object_or_404(RefbookVersion, refbook=refbook, version=version_str)
        else:
            today = datetime.today().date()
            version = RefbookVersion.objects.filter(refbook=refbook, start_date__lte=today).order_by(
                '-start_date').first()

        if not version:
            return Response({'valid': False}, status=status.HTTP_200_OK)

        element_exists = RefbookElement.objects.filter(version=version, code=code, value=value).exists()
        return Response({'valid': element_exists}, status=status.HTTP_200_OK)

