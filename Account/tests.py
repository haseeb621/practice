from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Bank.models import Bank

class AccountViewTests(TestCase):

    def setUp(self):
        # Set up a test client and test user
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword123',
            first_name='John', 
            last_name='Doe'
        )
        self.bank = Bank.objects.create(owner=self.user, name='Test Bank')

    def test_register_view(self):
        response = self.client.post(reverse('Account:register'), {
            'fname': 'John',
            'lname': 'Doe',
            'uname': 'newuser',
            'email': 'newuser@example.com',
            'pass1': 'newpassword123',
            'pass2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        response = self.client.post(reverse('Account:Login'), {
            'uname': 'testuser',
            'pass1': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('Account:success_login'))

    def test_success_login_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('Account:success_login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Bank')

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('Account:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "uname": "testuser",
            "email": "test@example.com",
            "fname": "John",
            "lname": "Doe",
            "pk": self.user.pk
        })

    def test_edit_profile_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('Account:edit_profile'), {
            'fname': 'Jane',
            'lname': 'Smith',
            'uname': 'testuser',
            'email': 'newemail@example.com',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Jane')
        self.assertEqual(self.user.last_name, 'Smith')
        self.assertEqual(self.user.email, 'newemail@example.com')

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('Account:Logout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Bank')

    def test_reset_pass_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('Account:reset_pass'), {
            'uname': 'testuser',
            'pass1': 'newpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))
