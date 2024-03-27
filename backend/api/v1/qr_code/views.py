from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.v1.qr_code.serializers import QRCodeSerializer
from apps.qr_code.models import QRCode


class QRCodeModelViewSet(viewsets.ModelViewSet):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer
    permission_classes = [permissions.IsAdminUser,]
    

    @swagger_auto_schema(
        method="get",
        operation_description="Получить список QR кодов",
        operation_summary="Получение списка QR кодов",
        operation_id="list_QRCode",
        tags=["QRCode"],
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
        operation_description="Обновление данных QR кодов",
        operation_summary="Обновление данных QR кодов",
        operation_id="update_QRCode",
        tags=["QRCode"],
        responses={
            200: openapi.Response(description="OK - QR код успешно обновлен"),
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
            qr_code = self.get_object()
            serializer = QRCodeSerializer(qr_code, data=request.data, partial=True)
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
        operation_description="Создание QR кода",
        operation_summary="Создание QR кода",
        operation_id="create_QRCode",
        tags=["QRCode"],
        responses={
            201: openapi.Response(description="Created - Новый QR код успешно создан"),
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
        operation_description="Удаление QR кода",
        operation_summary="Удаление QR кода",
        operation_id="delete_QRCode",
        tags=["QRCode"],
        responses={
            204: openapi.Response(description="No Content - QR код успешно удален"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - QR код не найден"),
        },
    )
    @action(detail=True, methods=["delete"])
    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except QRCode.DoesNotExist:
            return Response({"Сообщение": "QR код не найден"}, status=status.HTTP_404_NOT_FOUND)
