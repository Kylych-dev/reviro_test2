from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.pagination import PageNumberPagination


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.order.models import Order
from .serializers import OrderSerializer

from backend.api.utils.permissions import IsPartnerOrReadOnly

class OrderModelViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated,]


    @swagger_auto_schema(
        method="get",
        operation_description="Получить список заказов",
        operation_summary="Получение списка заказов",
        operation_id="list_order",
        tags=["Order"],
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
        operation_description="Обновление данных заказа",
        operation_summary="Обновление данных заказа",
        operation_id="update_order",
        tags=["Order"],
        responses={
            200: openapi.Response(description="OK - Заказ успешно обновлен"),
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
            instance = self.get_object()
            serializer = OrderSerializer(instance, data=request.data, partial=True)
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
        operation_description="Создание заказа",
        operation_summary="Создание заказа",
        operation_id="create_order",
        tags=["Order"],
        responses={
            201: openapi.Response(description="Created - Заказ успешно создан"),
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
        operation_description="Удаление заказа",
        operation_summary="Удаление заказа",
        operation_id="delete_order",
        tags=["Order"],
        responses={
            204: openapi.Response(description="No Content - Заказ успешно удален"),
            401: openapi.Response(description="Unauthorized - Неавторизованный запрос"),
            404: openapi.Response(description="Not Found - Заказ не найден"),
        },
    )
    @action(detail=True, methods=["delete"])
    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({"Сообщение": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)
