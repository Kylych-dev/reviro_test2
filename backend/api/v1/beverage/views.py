from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.beverage.models import Beverage
from api.utils.permissions import IsPartnerOrReadOnly
from .serializers import BeverageSerializer


class BeverageModelViewSet(viewsets.ModelViewSet):
    queryset = Beverage.objects.all()
    serializer_class = BeverageSerializer
    permission_classes = [permissions.IsAuthenticated, IsPartnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['availability_status']
    search_fields = ['name']

    '''
    name
    category
    price
    description
    availability_status
    establishment
    '''



    @swagger_auto_schema(
        # method="get",
        operation_description="Получить список напитков",
        operation_summary="Получение списка напитков",
        operation_id="list_beverage",
        tags=["Beverage"],
        responses={
            200: openapi.Response(description="OK - Список успешно получен"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())  # Применяем фильтры, если они заданы
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


    # @action(detail=True, method=["get"])
    # def list(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(self.queryset, many=True)
    #     return Response(serializer.data)

    @swagger_auto_schema(
        method="put",
        operation_description="Обновление данных напитка",
        operation_summary="Обновление данных напитка",
        operation_id="update_beverage",
        tags=["Beverage"],
        responses={
            200: openapi.Response(description="OK - Напиток успешно обновлен"),
            400: openapi.Response(
                description="Bad Request - Неверный запрос или некорректные данные"
            ),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    @action(detail=True, methods=["put"])
    def update(self, request, *args, **kwargs):
        try:
            beverage = self.get_object()
            serializer = BeverageSerializer(beverage, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, 
                    status=status.HTTP_200_OK
                    )
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as ex:
            return Response(
                {"Сообщение": str(ex)}, 
                status=status.HTTP_404_NOT_FOUND
                )

    @swagger_auto_schema(
        method="post",
        operation_description="Создание напитка",
        operation_summary="Создание напитка",
        operation_id="create_beverage",
        tags=["Beverage"],
        responses={
            201: openapi.Response(description="Created - Напиток успешно создан"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    @action(detail=True, methods=["post"])
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"Сообщение": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        method="delete",
        operation_description="Удаление напитка",
        operation_summary="Удаление напитка",
        operation_id="delete_beverage",
        tags=["Beverage"],
        responses={
            204: openapi.Response(description="No Content - Напиток успешно удален"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - напиток не найден"),
        },
    )
    @action(detail=True, methods=["delete"])
    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Beverage.DoesNotExist:
            return Response({"Сообщение": "Напиток не найден"}, status=status.HTTP_404_NOT_FOUND)







'''

http://127.0.0.1:3000/api/v1/beverage/create/

{
    "name": "Shoro",
    "category": "no alcohol",
    "price": 10.99,
    "description": "shoro company",
    "establishment": 1
}

'''