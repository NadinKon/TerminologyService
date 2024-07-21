from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Refbook, RefbookVersion, RefbookElement
from .serializers import RefbookSerializer, RefbookElementSerializer


class RefbookListView(APIView):
    @swagger_auto_schema(
        operation_description="Получение списка справочников",
        responses={200: RefbookSerializer(many=True)},  # Ответ будет сериализован RefbookSerializer
        manual_parameters=[
            openapi.Parameter('date', openapi.IN_QUERY, description="Дата начала действия в формате ГГГГ-ММ-ДД", type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request):
        # Получаем дату из параметров запроса, если она указана
        date_str = request.query_params.get('date', None)
        if date_str:
            # Преобразуем строку даты в объект даты
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            # Фильтруем справочники по дате начала действия
            refbooks = Refbook.objects.filter(versions__start_date__lte=date).distinct()
        else:
            # Если дата не указана, возвращаем все справочники
            refbooks = Refbook.objects.all()
        # Сериализуем данные справочников
        serializer = RefbookSerializer(refbooks, many=True)
        # Возвращаем ответ с сериализованными данными
        return Response({'refbooks': serializer.data}, status=status.HTTP_200_OK)


class RefbookElementListView(APIView):
    @swagger_auto_schema(
        operation_description="Получение элементов заданного справочника",
        responses={200: RefbookElementSerializer(many=True)},  # Ответ будет сериализован RefbookElementSerializer
        manual_parameters=[
            openapi.Parameter('version', openapi.IN_QUERY, description="Версия справочника", type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, id):
        # Получаем версию из параметров запроса, если она указана
        version_str = request.query_params.get('version', None)
        # Получаем справочник по его ID или возвращаем 404, если он не найден
        refbook = get_object_or_404(Refbook, pk=id)
        if version_str:
            # Получаем версию справочника по указанному значению
            version = get_object_or_404(RefbookVersion, refbook=refbook, version=version_str)
        else:
            # Если версия не указана, находим последнюю актуальную версию
            today = datetime.today().date()
            version = RefbookVersion.objects.filter(refbook=refbook, start_date__lte=today).order_by('-start_date').first()

        if not version:
            # Если версия не найдена, возвращаем пустой список элементов
            return Response({'elements': []}, status=status.HTTP_200_OK)

        # Получаем элементы указанной версии справочника
        elements = RefbookElement.objects.filter(version=version)
        # Сериализуем данные элементов
        serializer = RefbookElementSerializer(elements, many=True)
        # Возвращаем ответ с сериализованными данными
        return Response({'elements': serializer.data}, status=status.HTTP_200_OK)


class CheckElementView(APIView):
    @swagger_auto_schema(
        operation_description="Валидация элемента справочника",
        responses={200: openapi.Response('Valid or not', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'valid': openapi.Schema(type=openapi.TYPE_BOOLEAN)  # Описание возвращаемого значения (булево значение)
            }
        ))},
        manual_parameters=[
            openapi.Parameter('code', openapi.IN_QUERY, description="Код элемента справочника", type=openapi.TYPE_STRING),
            openapi.Parameter('value', openapi.IN_QUERY, description="Значение элемента справочника", type=openapi.TYPE_STRING),
            openapi.Parameter('version', openapi.IN_QUERY, description="Версия справочника", type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, id):
        # Получаем код и значение элемента из параметров запроса
        code = request.query_params.get('code')
        value = request.query_params.get('value')
        version_str = request.query_params.get('version', None)
        # Получаем справочник по его ID или возвращаем 404, если не найден
        refbook = get_object_or_404(Refbook, pk=id)

        if not code or not value:
            # Если код или значение не указаны, возвращаем 400
            return Response({'error': '***Code and value parameters are required'}, status=status.HTTP_400_BAD_REQUEST)

        if version_str:
            # Получаем версию справочника по указанному значению
            version = get_object_or_404(RefbookVersion, refbook=refbook, version=version_str)
        else:
            # Если версия не указана, находим последнюю актуальную версию
            today = datetime.today().date()
            version = RefbookVersion.objects.filter(refbook=refbook, start_date__lte=today).order_by('-start_date').first()

        if not version:
            # Если версия не найдена, возвращаем что элемент не валиден
            return Response({'valid': False}, status=status.HTTP_200_OK)

        # Проверяем, существует ли элемент с указанным кодом и значением в указанной версии справочника
        element_exists = RefbookElement.objects.filter(version=version, code=code, value=value).exists()
        # Возвращаем результат проверки
        return Response({'valid': element_exists}, status=status.HTTP_200_OK)
