from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.establishment.models import Establishment
from .serializers import EstablishmentSerializer



class EstablishmentModelViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer
    pagination_class = PageNumberPagination

    @swagger_auto_schema(
        method="get",
        operation_description="Получить список учреждений",
        operation_summary="Получение списка учреждений",
        operation_id="list_establishment",
        tags=["Establishment"],
        responses={
            200: openapi.Response(description="OK - Список успешно получен"),
            400: openapi.Response(description="Bad Request - Неверный запрос"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Ресурс не найден"),
        },
    )
    @action(detail=False, method=["get"])
    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        method="put",
        operation_description="Обновление данных учреждений",
        operation_summary="Обновление данных учреждений",
        operation_id="update_establishment",
        tags=["Establishment"],
        responses={
            200: openapi.Response(description="OK - Объект успешно обновлен"),
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
            establishment = self.get_object()
            serializer = EstablishmentSerializer(establishment, data=request.data, partial=True)
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
        operation_description="Создание учреждений",
        operation_summary="Создание учреждений",
        operation_id="create_establishment",
        tags=["Establishment"],
        responses={
            201: openapi.Response(description="Created - Новый учреждение успешно созданo"),
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
        operation_description="Удаление учреждения",
        operation_summary="Удаление учреждения",
        operation_id="delete_establishment",
        tags=["Establishment"],
        responses={
            204: openapi.Response(description="No Content - Учреждение успешно удален"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Учреждение не найден"),
        },
    )
    @action(detail=True, methods=["delete"])
    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Establishment.DoesNotExist:
            return Response({"Сообщение": "Учреждение не найден"}, status=status.HTTP_404_NOT_FOUND)
