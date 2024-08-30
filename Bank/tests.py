from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Bank.models import Bank, Branch

class BankViewTests(TestCase):

    def setUp(self):
        # Create a test client and test user
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
        self.bank = Bank.objects.create(name='Test Bank', description='A test bank', inst_num='123456', swift_code='ABCDEF', owner=self.user)
        self.branch = Branch.objects.create(name='Test Branch', transit_num='654321', email='branch@example.com', capacity=100, Bank_id=self.bank)

    def test_index_view(self):
        response = self.client.get(reverse('Bank:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Bank')

    def test_about_view(self):
        response = self.client.get(reverse('Bank:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_accounts_view(self):
        response = self.client.get(reverse('Bank:Accounts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts.html')

    def test_add_bank_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('Bank:add'), {
            'name': 'New Bank',
            'desc': 'New bank description',
            'inst_num': '789012',
            'swift_code': 'GHIJKL',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Bank.objects.filter(name='New Bank').exists())

    def test_delete_bank_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('Bank:delete_bank', args=[self.bank.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Bank.objects.filter(id=self.bank.id).exists())

    def test_add_branch_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('Bank:add_branch', args=[self.bank.id]), {
            'name': 'New Branch',
            'transit_num': '123123',
            'email': 'newbranch@example.com',
            'capacity': 200,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Branch.objects.filter(name='New Branch').exists())

    def test_branch_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('Bank:branch_view', args=[self.bank.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Branch')

    def test_branch_edit_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('Bank:branch_edit', args=[self.branch.id]), {
            'name': 'Updated Branch',
            'transit_num': '789456',
            'email': 'updatedbranch@example.com',
            'capacity': 150,
        })
        self.branch.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.branch.name, 'Updated Branch')
        self.assertEqual(self.branch.transit_num, '789456')
        self.assertEqual(self.branch.email, 'updatedbranch@example.com')
        self.assertEqual(self.branch.capacity, '150')
