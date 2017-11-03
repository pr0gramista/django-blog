from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from mistune import Markdown
from .models import Post, HeaderImage
from .markdown import PostRenderer, PostInlineLexer


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


class MarkdownEditorTests(TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        renderer = PostRenderer()
        inline = PostInlineLexer(renderer)
        inline.enable_woo()
        inline.enable_emdash()
        inline.enable_figure()

        self.markdown = Markdown(renderer, inline=inline, escape=False)

    def test_standard_markdown_tags(self):
        test_string = ("# h1\n"
                       "## h2\n"
                       "### h3\n"
                       "#### h4\n"
                       "##### h5\n"
                       "###### h6\n"
                       "*wow* **such markdown**\n"
                       "\n"
                       "> doge: markdown such intelligent\n"
                       "\n"
                       "[this is link](https://pr0gramista.pl)")
        output = self.markdown.render(test_string)

        correct_output = ("<h1>h1</h1>\n"
                          "<h2>h2</h2>\n"
                          "<h3>h3</h3>\n"
                          "<h4>h4</h4>\n"
                          "<h5>h5</h5>\n"
                          "<h6>h6</h6>\n"
                          "<p><em>wow</em> <strong>such markdown</strong></p>\n"
                          "<blockquote><p>doge: markdown such intelligent</p>\n"
                          "</blockquote>\n"
                          "<p><a href=\"https://pr0gramista.pl\">this is link</a></p>\n")

        self.assertHTMLEqual(output, correct_output)

    def test_custom_markdown_tags(self):
        test_string = ("This !-- is endash\n"
                       "![This is image](http://via.placeholder.com/350x150)\n"
                       "![This is a figure][This is a figure alt](http://via.placeholder.com/450x300)\n"
                       "!F[This is woo][done][FF0000][](https://docs.djangoproject.com/en/1.11/topics/testing/tools/)")
        output = self.markdown.render(test_string)

        correct_output = ("<p>This — is endash\n"
                          "<img src=\"http://via.placeholder.com/350x150\" alt=\"This is image\">\n"
                          "<figure><img src=\"http://via.placeholder.com/450x300\" alt=\"This is a figure alt\" /><div>This is a figure</div></figure>\n"
                          "\n"
                          "<div class=\"woo\">\n"
                          "  <div class=\"woo-fake\" style=\"background: #FF0000;\"></div>\n"
                          "  <a href=\"https://docs.djangoproject.com/en/1.11/topics/testing/tools/\"><div class=\"woo-content-wrapper\">\n"
                          "    <div class=\"woo-content \">\n"
                          "      <i class=\"material-icons\">done</i>\n"
                          "      <div>This is woo</div>\n"
                          "    </div>\n"
                          "  </div></a>\n"
                          "</div>")

        self.assertHTMLEqual(output, correct_output)