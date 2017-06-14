from django.test import TestCase, Client
from django.urls import reverse
from django.test.utils import setup_test_environment
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

example_image = SimpleUploadedFile(name='test.png', content=open('test.png', 'rb').read(), content_type='image/jpeg')

from .models import Post

def add_post(title, published, content):
    return Post.objects.create(
        title=title,
        slug=title.replace(' ','-')[0],
        title_size=42,
        title_background='rgba(0, 0, 0, 0.5)',
        image=example_image,
        pub_date=timezone.now(),
        published=published,
        raw_content=content,
        content=content)

class IndexViewTests(TestCase):
    def test_no_published_posts(self):
        """
        Unpublished posts should not be displayed in any form
        """
        add_post('Good post', True, 'This is a new content!')
        add_post('Nice post', True, 'This is a new content!')
        add_post('Bad post', False, 'This is a new content!')
        add_post('Awesome post', True, 'This is a new content!')

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['posts'],
            ['<Post: Awesome post>', '<Post: Nice post>', '<Post: Good post>']
        )

    def test_no_posts(self):
        """
        If no post exist, just don't display anything
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], [])


# Create your tests here.
