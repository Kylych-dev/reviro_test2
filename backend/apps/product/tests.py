from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.product.models import Product


class ProductModelViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(name="Test Product", description="Test Description", price=10.00, quantity_in_stock=5)
        self.valid_payload = {
            "name": "New Test Product",
            "description": "New Test Description",
            "price": 15.00,
            "quantity_in_stock": 8
        }
        self.invalid_payload = {
            "name": "",
            "description": "New Test Description",
            "price": 15.00,
            "quantity_in_stock": 8
        }

    def test_list_products(self):
        response = self.client.get(reverse("product-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        response = self.client.post(reverse("product-create"), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_invalid_payload(self):
        response = self.client.post(reverse("product-create"), data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product(self):
        url = reverse("product-update", kwargs={"pk": self.product.pk})
        response = self.client.put(url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        url = reverse("product-delete", kwargs={"pk": self.product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
