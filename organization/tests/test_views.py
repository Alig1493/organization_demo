from django.test import TestCase
import factory
from django.urls import reverse
from rest_framework.test import APIClient

from organization.tests import UserFactory, OrganizationFactory, IFrameFactory


class TestIFrame(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.organization = OrganizationFactory()
        self.user = UserFactory()
        self.url = "http://127.0.0.1:8000/docs/"

    def test_add_iframe(self):
        self.client.force_authenticate(user=self.user)
        self.organization.user = [self.user]
        self.organization.save()
        url = reverse('organization:iframe_list_create')
        iframe = factory.build(dict, FACTORY_CLASS=IFrameFactory)
        # invalid url
        iframe['url'] = "asdasdasdasd"
        iframe['user'] = self.user
        request = self.client.post(url, iframe)
        # should fail test for invalid url
        self.assertEqual(request.status_code, 400)
        self.assertEqual(request.data['url'][0], "Enter a valid URL.")
        # valid url
        iframe['url'] = self.url
        request = self.client.post(url, iframe)
        # should pass test and create an IFrame object
        self.assertEqual(request.status_code, 201)

    def test_modify_iframe(self):
        self.client.force_authenticate(user=self.user)
        self.organization.user = [self.user]
        self.organization.save()
        iframe = IFrameFactory(organization=self.organization, url=self.url)
        url = reverse('organization:iframe_details', args=[iframe.id])
        title = 'something else'
        request = self.client.patch(url, {'title': title})
        # should pass test if user of same organization tries to modify organization links
        self.assertEqual(request.status_code, 200)
        # same for delete
        request = self.client.delete(url)
        self.assertEqual(request.status_code, 204)

    def test_modify_iframe_by_outside(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        organization = OrganizationFactory(user=[user])
        iframe = IFrameFactory(organization=self.organization, url=self.url)
        url = reverse('organization:iframe_details', args=[iframe.id])
        title = 'something else'
        request = self.client.patch(url, {'title': title})
        # should fail test if user of another organization tries to modify organization links
        self.assertEqual(request.status_code, 404)
        # same for delete
        request = self.client.delete(url)
        self.assertEqual(request.status_code, 404)
