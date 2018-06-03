from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User


class QuestionAnswerTests(TestCase):
    """Main views testing class."""

    def setUp(self):
        """Test initialization."""
        self.client = Client()

    def test_redirect_if_not_logged_in(self):
        """
        Redirect to login page if not logged in.

        User is redirected to login page when he/she
        tries to access index page prior to logging in
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('login' in response.url)

    def test_successful_signup(self):
        """
        Redirect to index page if signup is successful.

        After successful signup user is redirected
        to index page.
        """
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'SecurePassw0rd',
            'password2': 'SecurePassw0rd'
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_not_successful_signup(self):
        """Attempt to sign up with not matching passwords."""
        data = {
            'first_name': 'John',
            'last_name': 'Smith',
            'password1': 'SecurePassw0rd123',
            'password2': 'SecurePassw0rd'
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "The two password fields didn&#39;t match" in response.content
        )

    def test_logout(self):
        """
        Log out the logged in user.

        After successfull signup user is logged in.
        After logout user is redirected to login page.
        """
        self.test_successful_signup()
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('login' in response.url)

    def test_successful_login(self):
        """
        Successful login test.

        Create a user, login with the new user credentials
        and make sure that user's first name is displayed
        on the redirected page.
        """
        User.objects.create_user(
            'John_Doe', 'admin@test.com',
            'pass', first_name='John', last_name='Doe'
        )
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'pass',
        }
        response = self.client.post(reverse('login'), data, follow=True)
        self.assertTrue('Welcome, John' in response.content)
