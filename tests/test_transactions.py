from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser


class TransactionTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = CustomUser.objects.create_user(
            username='testadmin', password='pass123', role='admin'
        )
        self.viewer = CustomUser.objects.create_user(
            username='testviewer', password='pass123', role='viewer'
        )

    def get_token(self, username, password):
        res = self.client.post('/api/auth/login/',
            {'username': username, 'password': password}, format='json')
        return res.data.get('access')

    def test_login_success(self):
        token = self.get_token('testadmin', 'pass123')
        self.assertIsNotNone(token)

    def test_login_wrong_password(self):
        res = self.client.post('/api/auth/login/',
            {'username': 'testadmin', 'password': 'wrong'}, format='json')
        self.assertEqual(res.status_code, 401)

    def test_admin_can_create_transaction(self):
        token = self.get_token('testadmin', 'pass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        res = self.client.post('/api/transactions/',
            {'amount': 1000, 'type': 'income', 'category': 'Test', 'date': '2024-01-01'},
            format='json')
        self.assertEqual(res.status_code, 201)

    def test_viewer_cannot_create_transaction(self):
        token = self.get_token('testviewer', 'pass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        res = self.client.post('/api/transactions/',
            {'amount': 100, 'type': 'income', 'category': 'Test', 'date': '2024-01-01'},
            format='json')
        self.assertEqual(res.status_code, 403)

    def test_invalid_amount_rejected(self):
        token = self.get_token('testadmin', 'pass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        res = self.client.post('/api/transactions/',
            {'amount': -500, 'type': 'income', 'category': 'Bad', 'date': '2024-01-01'},
            format='json')
        self.assertEqual(res.status_code, 400)

    def test_list_transactions(self):
        token = self.get_token('testadmin', 'pass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        res = self.client.get('/api/transactions/')
        self.assertEqual(res.status_code, 200)