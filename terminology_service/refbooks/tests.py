from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Refbook, RefbookVersion, RefbookElement


class RefbookAPITestCase(APITestCase):

    def setUp(self):
        self.refbook = Refbook.objects.create(code="TEST1", name="Test Refbook", description="Test Description")
        self.version = RefbookVersion.objects.create(refbook=self.refbook, version="1.0", start_date="2023-01-01")
        self.element = RefbookElement.objects.create(version=self.version, code="E1", value="Element 1")

    def test_get_refbooks(self):
        url = reverse('refbook-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['refbooks']), 1)
        self.assertEqual(response.data['refbooks'][0]['code'], "TEST1")

    def test_get_refbook_elements(self):
        url = reverse('refbook-element-list', args=[self.refbook.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['elements']), 1)
        self.assertEqual(response.data['elements'][0]['code'], "E1")

    def test_check_element(self):
        url = reverse('refbook-check-element', args=[self.refbook.id])
        response = self.client.get(url, {'code': 'E1', 'value': 'Element 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['valid'])
