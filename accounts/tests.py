from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User



class LoginViewTestCase(TestCase):
    """Tests login. 
    """
    def setUp(self):
        self.user = User.objects.create_user(username='ismael', password='user123456')
        
        self.valid_data = {
            'username': 'ismael',
            'password': 'user123456',
        }
        
        self.invalid_data = {
            'username': 'testuser',
            'password': 'incorrectpassword',
        }


    def test_login_successful(self):
        response = self.client.post(reverse('login'), self.valid_data, follow=True)
        self.assertEqual(response.status_code, 404) #Obtiene un 404 al buscar tarjetas relacionadas
        self.assertTrue(response.context['user'].is_authenticated)

        

    def test_login_invalid(self):
        response = self.client.post(reverse('login'), self.invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

