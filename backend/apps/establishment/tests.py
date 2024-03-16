from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.establishment.models import Establishment


class EstablishmentModelViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.establishment = Establishment.objects.create(
            name="Test Establishment",
            description="Test Description",
            locations="Test Locations",
            opening_hours="Test Hours",
            requirements="Test Requirements"
        )
        self.valid_payload = {
            "name": "New Test Establishment",
            "description": "New Test Description",
            "locations": "New Test Locations",
            "opening_hours": "New Test Hours",
            "requirements": "New Test Requirements"
        }
        self.invalid_payload = {
            "name": "",
            "description": "New Test Description",
            "locations": "New Test Locations",
            "opening_hours": "New Test Hours",
            "requirements": "New Test Requirements"
        }

    def test_list_establishments(self):
        response = self.client.get(reverse("establishment-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_establishment(self):
        response = self.client.post(reverse("establishment-create"), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_establishment_invalid_payload(self):
        response = self.client.post(reverse("establishment-create"), data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_establishment(self):
        url = reverse("establishment-update", kwargs={"pk": self.establishment.pk})
        response = self.client.put(url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_establishment(self):
        url = reverse("establishment-delete", kwargs={"pk": self.establishment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
