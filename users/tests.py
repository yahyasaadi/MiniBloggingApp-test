from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Blog  # Import your Blog model
from .serializers import BlogSerializer

class BlogListTestCase(TestCase):
    def setUp(self):
        # Create a test user and some blog objects for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')

        self.blog1 = Blog.objects.create(title='Blog 1', content='Content 1', author=self.user)
        self.blog2 = Blog.objects.create(title='Blog 2', content='Content 2', author=self.user)

    def test_blog_list_view(self):
        # Ensure the view returns HTTP 200 OK and the expected data
        url = reverse('all-blogs')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # You may need to customize this part based on your serializer's output
        expected_data = [
            {
                'id': self.blog1.id,
                'title': self.blog1.title,
                'content': self.blog1.content,
                'created_at': self.blog1.created_at.strftime('%B %d, %Y %I:%M %p'),
                'author': self.blog1.author.username,
            },
            {
                'id': self.blog2.id,
                'title': self.blog2.title,
                'content': self.blog2.content,
                'created_at': self.blog2.created_at.strftime('%B %d, %Y %I:%M %p'),
                'author': self.blog2.author.username,
            },
        ]
        self.assertEqual(response.data, expected_data)

    def tearDown(self):
        # Clean up test data
        self.client.logout()
        self.user.delete()
        self.blog1.delete()
        self.blog2.delete()

