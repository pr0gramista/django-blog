from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from .models import Post, HeaderImage

example_image = SimpleUploadedFile(name='test.png', content=open(
    'test.png', 'rb').read(), content_type='image/jpeg')


def get_test_user_tom():
    return User.objects.create_user('tom', 'tom@tomland.tomland', 'tomsecuredpassword')


def add_post(title, published, content, fullwidth=True):
    """
    Create and return post with given arguments

    :param title: Title for post
    :type title: string
    :param published: should post be published
    :type published: boolean
    :param content: final content of the post
    :type content: string
    """
    headerImage = HeaderImage.objects.create(
        image=example_image
    )

    return Post.objects.create(
        title=title,
        slug=title.replace(' ', '-')[0],
        title_size=42,
        title_background='rgba(0, 0, 0, 0.5)',
        image=headerImage,
        pub_date=timezone.now(),
        published=published,
        fullwidth=fullwidth,
        raw_content=content,
        content=content)


class IndexViewTests(TestCase):
    def test_no_private_posts(self):
        """Unpublished posts should not be displayed in any form."""
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

    def test_private_posts_when_logged_in(self):
        """
        If user is logged in all posts should be displayed
        """
        self.client.force_login(get_test_user_tom())
        add_post('Good post', True, 'This is a new content!')
        add_post('Nice post', True, 'This is a new content!')
        add_post('Bad post', False, 'This is a new content!')
        add_post('Awesome post', True, 'This is a new content!')

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['posts'],
            ['<Post: Awesome post>', '<Post: Bad post>', '<Post: Nice post>', '<Post: Good post>'])


class PostViewTests(TestCase):
    def test_published_post(self):
        post = add_post('good post', True, 'This is a public post')

        response = self.client.get(reverse('post', args=post.slug))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual([response.context['post']], ['<Post: good post>'])

    def test_fullwidth_post(self):
        post = add_post('good post', True, 'This is public post', fullwidth=True)
        response = self.client.get(reverse('post', args=post.slug))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            any(x for x in response.templates if '/base-fullwidth.html' in x.name),
            True)

    def test_no_fullwidth_post(self):
        post = add_post('bad post', True, 'This is public post', fullwidth=False)
        response = self.client.get(reverse('post', args=post.slug))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            any(x for x in response.templates if '/base-fullwidth.html' in x.name),
            False)

    def test_no_private_post(self):
        """
        Unpublished post should not be displayed in any form for unauthorized users
        """
        post = add_post('bad post', False, 'This is a private post')

        response = self.client.get(reverse('post', args=post.slug))
        self.assertEqual(response.status_code, 404)

    def test_private_post_when_logged_in(self):
        """
        Unpublished post should displayed for logged in user
        """
        self.client.force_login(get_test_user_tom())
        post = add_post('bad post', False, 'This is a private post')

        response = self.client.get(reverse('post', args=post.slug))
        self.assertEqual(response.status_code, 200)
