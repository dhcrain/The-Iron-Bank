from django.test import TestCase
from bank_app.models import Transaction
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client


class TransactionModelTest(TestCase):

    def test_string_representation(self):
        transaction = Transaction(payee="the man")
        self.assertEqual(str(transaction), transaction.payee)


class ProjectTests(TestCase):

    def test_homepage(self):
        response = self.client.get(reverse('index_view'))
        self.assertEqual(response.status_code, 200)


class TestLoginRequired(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_redirects_to_login_page_on_not_loggedin(self):
        response = self.client.get(reverse('transfer_view'))
        print(response)
        self.assertRedirects(response, '/login/?next=/account/transfer')

    def test_redirects_to_test_page_on_loggedin(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('transfer_view'))
        self.assertEqual(response.status_code, 200)
        # self.assertRedirects(response, reverse('transfer_view'))


class TransactionPageTests(TestCase):

    """Test whether Transaction entries show up on the account page and login"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_one_entry(self):
        Transaction.objects.create(amount=123.45, payee="Jim Bob", user=self.user)
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('account_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 123.45)
        self.assertContains(response, "Jim Bob")

    def test_two_entries(self):
        Transaction.objects.create(amount=123.45, payee="Jim Bob", user=self.user)
        Transaction.objects.create(amount=567.98, payee="Sam Bo", user=self.user)
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('account_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 123.45)
        self.assertContains(response, 567.98)
        self.assertContains(response, "Sam Bo")
        # Test for total
        self.assertContains(response, round((123.45 + 567.98), 2))
