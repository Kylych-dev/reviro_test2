from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.establishment.views import EstablishmentModelViewSet
from api.v1.accounts.views import RegularUserUpdateView, PartnerUpdateView
from api.v1.beverage.views import BeverageModelViewSet
from api.v1.order.views import OrderModelViewSet
from api.v1.qr_code.views import QRCodeModelViewSet 

from api.auth.views import (
    PartnerRegistrationView, 
    RegularUserRegistrationView, 
    UserAuthenticationView, 
    UserRegistrationView
    )

router = DefaultRouter(trailing_slash=False)

urlpatterns = router.urls

urlpatterns.extend(
    [   
        # Auth
        path('register/partner/', PartnerRegistrationView.as_view(), name='partner-registration'),
        path('register/admin/', UserRegistrationView.as_view(), name='admin_registration'),
        path('register/user/', RegularUserRegistrationView.as_view(), name='user-registration'),

        path('login/', UserAuthenticationView.as_view({"post": "login"}), name='user-login'),
        path('logout/', UserAuthenticationView.as_view({"post": "logout"}), name='user-logout'),

        # user
        # path("users/", CustomUserViewSet.as_view({"get": "list"}), name="user-list"),
        # path("users/profile/", CustomUserViewSet.as_view({"get": "user_profile"}), name="user-profile"),
        # path("users/<slug:slug>/", CustomUserViewSet.as_view({"get": "user_detail"}), name="user-detail"),
        # path("users/<slug:slug>/", RegularUserUpdateView.as_view({"put": "update_detail"}), name="update-detail"),
        path("users_update/<int:pk>/", RegularUserUpdateView.as_view(), name="update-detail"),
        path("partner_update/<int:pk>/", PartnerUpdateView.as_view(), name="update-detail"),

        


        # Beverage
        path("beverage/", BeverageModelViewSet.as_view({"get": "list"}), name="beverage-list"),
        path("beverage/create/", BeverageModelViewSet.as_view({"post": "create"}), name="beverage-create"),
        path("beverage/update/<uuid:pk>/", BeverageModelViewSet.as_view({"put": "update"}), name="beverage-update"),
        path("beverage/delete/<uuid:pk>/", BeverageModelViewSet.as_view({"delete": "delete"}), name="beverage-delete"),

        # Establishment
        path("establishment/", EstablishmentModelViewSet.as_view({"get": "list"}), name="establishment-list"),
        path("establishment/create/", EstablishmentModelViewSet.as_view({"post": "create"}), name="establishment-create"),
        path("establishment/update/<uuid:pk>/", EstablishmentModelViewSet.as_view({"put": "update"}), name="establishment-update"),
        path("establishment/delete/<uuid:pk>/",EstablishmentModelViewSet.as_view({"delete": "delete"}), name="establishment-delete"),

        # Order
        path("order/", OrderModelViewSet.as_view({"get": "list"}), name="order-list"),
        path("order/create/", OrderModelViewSet.as_view({"post": "create"}), name="order-create"),
        path("order/update/<uuid:pk>/", OrderModelViewSet.as_view({"put": "update"}), name="order-update"),
        path("order/delete/<uuid:pk>/",OrderModelViewSet.as_view({"delete": "delete"}), name="order-delete"),

        # QR Code
        path("qr_code/", QRCodeModelViewSet.as_view({"get": "list"}), name="qr_code-list"),
        path("qr_code/create/", QRCodeModelViewSet.as_view({"post": "create"}), name="qr_code-create"),
        path("qr_code/update/<uuid:pk>/", QRCodeModelViewSet.as_view({"put": "update"}), name="qr_code-update"),
        path("qr_code/delete/<uuid:pk>/",QRCodeModelViewSet.as_view({"delete": "delete"}), name="qr_code-delete"),

        
    
        # product
        # path("product/", ProductModelViewSet.as_view({"get": "list"}), name="product-list"),
        # path("product/create/", ProductModelViewSet.as_view({"post": "create"}), name="product-create"),
        # path("product/update/<pk>/", ProductModelViewSet.as_view({"put": "update"}), name="product-update"),
        # path("product/delete/<pk>/",ProductModelViewSet.as_view({"delete": "delete"}), name="product-delete"),     
    ]
)