from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from rest_framework import status
from sports_events.core import models
# Create your tests here.


class TestRespStatus(APITestCase):
    def setUp(self):
        url = reverse('all_matches')
        data = {
            "id": 8661032861909884224,
            "message_type": "NewEvent",
            "event": {
                "id": 123,
                "name": "Real Madrid vs Barcelona",
                "startTime": "2018-06-20 10:30:00",
                "sport": {
                        "id": 220,
                        "name": "Football"
                },
                "markets": [{
                    "id": 1234,
                    "name": "Winner",
                    "selections": [
                        {
                            "id": 9999,
                            "name": "Real Madrid",
                            "odds": 10.00
                        }, {
                            "id": 123,
                            "name": "Barcelona",
                            "odds": 5.55
                        }
                    ]
                }]
            }
        }
        resp = self.client.post(url, data, format="json")

    def test_get(self):
        url = reverse('all_matches')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_match(self):
        url = reverse('match', kwargs={'id': '123'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_invalid_match(self):
        url = reverse('match', kwargs={'id': '1234'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_post_bad_param(self):
        url = reverse('all_matches')
        data = {}
        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_post_create(self):
        url = reverse('all_matches')
        data = {
            "id": 8661032861909884224,
            "message_type": "NewEvent",
            "event": {
                "id": 994839351740,
                "name": "Real Madrid vs Barcelona",
                "startTime": "2018-06-20 10:30:00",
                "sport": {
                        "id": 221,
                        "name": "Football"
                },
                "markets": [{
                    "id": 385086549360973392,
                    "name": "Winner",
                    "selections": [
                        {
                            "id": 8243901714083343527,
                            "name": "Real Madrid",
                            "odds": 10.00
                        }, {
                            "id": 5737666888266680774,
                            "name": "Barcelona",
                            "odds": 5.55
                        }
                    ]
                }]
            }
        }
        resp = self.client.post(url, data, format="json")
        models.Sports.objects.filter(id=221).delete()
        models.Events.objects.filter(id=994839351740).delete()
        models.Selection.objects.filter(event=994839351740).delete()
        models.Markets.objects.filter(id=385086549360973392).delete()

        resp_status = {'status': True}
        self.assertEqual(resp.status_code, 200)
        self.assertEquals(resp_status, resp.json())

    def test_post_create_bad_req(self):
        url = reverse('all_matches')
        data = {
            "id": 8661032861909884224,
            "message_type": "NewEvent",
            "event": {
                "id": 994839351740,
                "name": "Real Madrid vs Barcelona",
                "startTime": "2018-06-20 10:30:00",
                "sport": {
                            "id": 221,
                            "name": "Football"
                },
                "markets": [{
                    "id": 385086549360973392,
                    "name": "Winner",
                    "selections": [
                    ]
                }]
            }
        }
        resp = self.client.post(url, data, format="json")
        models.Sports.objects.filter(id=221).delete()
        models.Events.objects.filter(id=994839351740).delete()
        models.Selection.objects.filter(event=994839351740).delete()
        models.Markets.objects.filter(id=385086549360973392).delete()

        resp_status = {
            'error': 'Selections must be of length 2', 'status': False}
        self.assertEqual(resp.status_code, 400)
        self.assertEquals(resp_status, resp.json())


class SearchFootabll(APITestCase):
    def test_create_account(self):
        """
                        Tests Football search Field
        """
        url = reverse('all_matches')
        url += "?search=football"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestMatchCreate(APITestCase):

    def test_new_event(self):
        url = reverse('all_matches')
        data = {
            "id": 8661032861909884224,
            "message_type": "NewEvent",
            "event": {
                            "id": 994839351740,
                            "name": "Real Madrid vs Barcelona",
                "startTime": "2018-06-20 10:30:00",
                "sport": {
                    "id": 221,
                    "name": "Football"
                },
                "markets": [{
                    "id": 385086549360973392,
                    "name": "Winner",
                    "selections": [
                        {
                            "id": 8243901714083343527,
                            "name": "Real Madrid",
                            "odds": 10.00
                        }, {
                            "id": 5737666888266680774,
                            "name": "Barcelona",
                            "odds": 5.55
                        }
                    ]
                }]
            }
        }
        resp = self.client.post(url, data, format="json")
        models.Sports.objects.filter(id=221).delete()
        models.Events.objects.filter(id=994839351740).delete()
        models.Selection.objects.filter(event=994839351740).delete()
        models.Markets.objects.filter(id=385086549360973392).delete()

        resp_status = {'status': True}
        self.assertEqual(resp.status_code, 200)
        self.assertEquals(resp_status, resp.json())

    def test_invalid_message(self):
        url = reverse('all_matches')
        data = {
            "id": 8661032861909884224,
            "message_type": "AddEvent",
            "event": {
                "id": 994839351740,
                "name": "Real Madrid vs Barcelona",
                "startTime": "2018-06-20 10:30:00",
                "sport": {
                    "id": 221,
                    "name": "Football"
                },
                "markets": [{
                    "id": 385086549360973392,
                    "name": "Winner",
                    "selections": [
                        {
                            "id": 8243901714083343527,
                            "name": "Real Madrid",
                            "odds": 10.00
                        }, {
                            "id": 5737666888266680774,
                            "name": "Barcelona",
                            "odds": 5.55
                        }
                    ]
                }]
            }
        }
        resp = self.client.post(url, data, format="json")
        models.Sports.objects.filter(id=221).delete()
        models.Events.objects.filter(id=994839351740).delete()
        models.Selection.objects.filter(event=994839351740).delete()
        models.Markets.objects.filter(id=385086549360973392).delete()

        resp_status = {'message': 'Invalid Message Type', 'status': False}
        self.assertEqual(resp.status_code, 400)
        self.assertEquals(resp_status, resp.json())

    def test_update_odds(self):

        # create Event
        url = reverse('all_matches')
        data = {
            "id": 8661032861909884224,
            "message_type": "NewEvent",
            "event": {
                "id": 994839351740,
                "name": "Real Madrid vs Barcelona",
                "startTime": "2018-06-20 10:30:00",
                "sport": {
                    "id": 221,
                    "name": "Football"
                },
                "markets": [{
                    "id": 385086549360973392,
                    "name": "Winner",
                    "selections": [
                        {
                            "id": 8243901714083343527,
                            "name": "Real Madrid",
                            "odds": 10.00
                        }, {
                            "id": 5737666888266680774,
                            "name": "Barcelona",
                            "odds": 5.55
                        }
                    ]
                }]
            }
        }
        resp = self.client.post(url, data, format="json")
        # Update Event
        url = reverse('all_matches')
        data = {
            "id": 8661032861909884224,
            "message_type": "UpdateOdds",
            "event": {
                "id": 994839351740,
                "name": "Real Madrid vs Barcelona",
                "startTime": "2018-06-20 10:30:00",
                "sport": {
                    "id": 221,
                    "name": "Football"
                },
                "markets": [{
                    "id": 385086549360973392,
                    "name": "Winner",
                    "selections": [
                        {
                            "id": 8243901714083343527,
                            "name": "Real Madrid",
                            "odds": 10.00
                        }, {
                            "id": 5737666888266680774,
                            "name": "Barcelona",
                            "odds": 5.55
                        }
                    ]
                }]
            }
        }
        resp = self.client.post(url, data, format="json")
        models.Sports.objects.filter(id=221).delete()
        models.Events.objects.filter(id=994839351740).delete()
        models.Selection.objects.filter(event=994839351740).delete()
        models.Markets.objects.filter(id=385086549360973392).delete()

        resp_status = {'status': True}
        self.assertEqual(resp.status_code, 200)
        self.assertEquals(resp_status, resp.json())
