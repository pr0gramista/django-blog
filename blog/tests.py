import xml.etree.ElementTree

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from mistune import Markdown
from taggit.models import Tag

from .markdown import PostRenderer, PostInlineLexer
from .models import Post, HeaderImage, Page

example_image = SimpleUploadedFile(name='test.png', content=open(
    'test.png', 'rb').read(), content_type='image/jpeg')


def get_test_user_tom():
    return User.objects.create_user('tom', 'tom@tomland.tomland', 'tomsecuredpassword')


def add_post(title, published, content, fullwidth=True, tags=None):
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

    post = Post.objects.create(
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

    if tags is not None:
        post.tags.add(*tags)

    return post


class IndexViewTests(TestCase):
    def setUp(self):
        from . import views
        views.POSTS_PER_PAGE = 5

    def test_no_private_posts(self):
        """Unpublished posts should not be displayed in any form."""
        add_post('Good post', True, 'This is a new content!')
        add_post('Nice post', True, 'This is a new content!')
        add_post('Bad post', False, 'This is a new content!')
        add_post('Awesome post', True, 'This is a new content!')

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/index.html")
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
        self.assertTemplateUsed(response, "blog/index.html")
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
        self.assertTemplateUsed(response, "blog/index.html")
        self.assertQuerysetEqual(
            response.context['posts'],
            ['<Post: Awesome post>', '<Post: Bad post>', '<Post: Nice post>', '<Post: Good post>'])


class PaginationSpecificTests(TestCase):
    def setUp(self):
        from . import views
        views.POSTS_PER_PAGE = 2

    def test_pagination_10(self):
        """Pagination should display only as many posts as defined in views.py POST_PER_PAGE"""

        for n in range(1, 30):
            add_post('Post ' + str(n), True, 'This is test content!')

        response = self.client.get(reverse('index_pagination', args=[10]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/index.html")
        self.assertQuerysetEqual(
            response.context['posts'],
            ['<Post: Post 11>', '<Post: Post 10>', ]
        )

    def test_limit_pagination(self):
        """Pagination should display only as many posts as defined in views.py POST_PER_PAGE"""

        for n in range(1, 7):  # 6 posts
            add_post('Post ' + str(n), True, 'This is test content!')

        response = self.client.get(reverse('index_pagination', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/index.html")
        self.assertQuerysetEqual(
            response.context['posts'],
            ['<Post: Post 4>', '<Post: Post 3>', ]
        )

    def test_limit_tag_pagination(self):
        """Pagination should display only as many posts as defined in views.py POST_PER_PAGE"""
        test_tag = Tag.objects.create(name="Test", slug="test")

        for n in range(1, 6):  # 5 posts
            add_post('Post ' + str(n), True, 'This is test content!', tags=[test_tag])

        response = self.client.get(reverse('tag_pagination', args=[test_tag.slug, 2]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/tag.html")
        self.assertQuerysetEqual(
            response.context['posts'],
            ['<Post: Post 3>', '<Post: Post 2>', ]
        )


class PostViewTests(TestCase):
    def test_published_post(self):
        post = add_post('good post', True, 'This is a public post')

        response = self.client.get(reverse('post', args=post.slug))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual([response.context['post']], ['<Post: good post>'])
        self.assertTemplateUsed(response, "blog/post.html")
        self.assertEqual(response.context['post'].title, 'good post')

    def test_fullwidth_post(self):
        post = add_post('good post', True, 'This is public post', fullwidth=True)
        response = self.client.get(reverse('post', args=post.slug))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            any(x for x in response.templates if '/base-fullwidth.html' in x.name),
            True)
        self.assertTemplateUsed(response, "blog/post.html")
        self.assertEqual(response.context['post'].title, 'good post')

    def test_no_fullwidth_post(self):
        post = add_post('bad post', True, 'This is public post', fullwidth=False)
        response = self.client.get(reverse('post', args=post.slug))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            any(x for x in response.templates if '/base-fullwidth.html' in x.name),
            False)
        self.assertTemplateUsed(response, "blog/post.html")
        self.assertEqual(response.context['post'].title, 'bad post')

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


class PageTests(TestCase):
    def test_page_ok(self):
        """Check if page renders correctly"""
        page = Page.objects.create(title="Test page", slug="test-page", content="It better works, "
                                                                                "or I am screwed")
        response = self.client.get(reverse('page', args=[page.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/page.html')
        self.assertEqual(response.context['page'], page)


class UtilityTests(TestCase):
    def test_youtube_redirection_ok(self):
        response = self.client.get('/youtube')
        self.assertRedirects(response, 'https://www.youtube.com/channel/UCHPUGfK2zW0VUNN2SgCHsXg', fetch_redirect_response=False)


class TagTests(TestCase):
    def setUp(self):
        from . import views
        views.POSTS_PER_PAGE = 5

    def test_no_private_posts(self):
        """Unpublished posts should not be displayed in any form."""
        test_tag = Tag.objects.create(name="Test", slug="test")

        add_post('Good post', True, 'This is a new content!', tags=[test_tag])
        add_post('Nice post', True, 'This is a new content!', tags=[test_tag])
        add_post('Bad post', False, 'This is a new content!', tags=[test_tag])
        add_post('Awesome post', True, 'This is a new content!', tags=[test_tag])

        response = self.client.get(reverse('tag', args=[test_tag.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/tag.html")
        self.assertQuerysetEqual(
            response.context['posts'],
            ['<Post: Awesome post>', '<Post: Nice post>', '<Post: Good post>']
        )

    def test_no_posts(self):
        """
        If no post exist, just don't display anything
        """
        test_tag = Tag.objects.create(name="Test", slug="test")

        response = self.client.get(reverse('tag', args=[test_tag.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/tag.html")
        self.assertQuerysetEqual(response.context['posts'], [])

    def test_private_posts_when_logged_in(self):
        """
        If user is logged in all posts should be displayed
        """
        test_tag = Tag.objects.create(name="Test", slug="test")

        self.client.force_login(get_test_user_tom())
        add_post('Good post', True, 'This is a new content!', tags=[test_tag])
        add_post('Nice post', True, 'This is a new content!', tags=[test_tag])
        add_post('Bad post', False, 'This is a new content!', tags=[test_tag])
        add_post('Awesome post', True, 'This is a new content!', tags=[test_tag])

        response = self.client.get(reverse('tag', args=[test_tag.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/tag.html")
        self.assertQuerysetEqual(
            response.context['posts'],
            ['<Post: Awesome post>', '<Post: Bad post>', '<Post: Nice post>',
             '<Post: Good post>'])


class RSSTests(TestCase):
    def test_no_private_posts(self):
        """Unpublished posts should not be present in XML."""
        add_post('Good post', True, 'This is a new content!')
        add_post('Nice post', True, 'This is a new content!')
        add_post('Bad post', False, 'This is a new content!')
        add_post('Awesome post', True, 'This is a new content!')

        response = self.client.get(reverse('rss_index'))
        self.assertEqual(response.status_code, 200)

        root = xml.etree.ElementTree.fromstring(response.content)
        # Extract titles from posts as RSS (dirty)
        titles = [[tag.text.strip() for tag in child if tag.tag == 'title'][0]
                  for child in root[0] if child.tag == 'item']

        self.assertNotIn('Bad post', titles)

    def test_no_private_posts_tag(self):
        """Unpublished posts should not be present in XML."""
        test_tag = Tag.objects.create(name="Test", slug="test")

        add_post('Good post', True, 'This is a new content!', tags=[test_tag])
        add_post('Nice post', True, 'This is a new content!', tags=[test_tag])
        add_post('Bad post', False, 'This is a new content!', tags=[test_tag])
        add_post('Awesome post', True, 'This is a new content!', tags=[test_tag])

        response = self.client.get(reverse('rss_tag', args=[test_tag.slug]))
        self.assertEqual(response.status_code, 200)

        root = xml.etree.ElementTree.fromstring(response.content)
        # Extract titles from posts as RSS (dirty)
        titles = [[tag.text.strip() for tag in child if tag.tag == 'title'][0]
                  for child in root[0] if child.tag == 'item']

        self.assertNotIn('Bad post', titles)


class MarkdownEditorTests(TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        renderer = PostRenderer()
        inline = PostInlineLexer(renderer)
        inline.enable_woo()
        inline.enable_emdash()
        inline.enable_figure()
        inline.enable_gallery()

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
                       "![This is a figure][This is a figure alt]("
                       "http://via.placeholder.com/450x300)\n"
                       "!F[This is woo][done][FF0000][]("
                       "https://docs.djangoproject.com/en/1.11/topics/testing/tools/)")
        output = self.markdown.render(test_string)

        correct_output = ("<p>This — is endash\n"
                          "<img src=\"http://via.placeholder.com/350x150\" alt=\"This is image\">\n"
                          "<figure><img src=\"http://via.placeholder.com/450x300\" alt=\"This is "
                          "a figure alt\" /><div>This is a figure</div></figure>\n"
                          "\n"
                          "<div class=\"woo\">\n"
                          "  <div class=\"woo-fake\" style=\"background: #FF0000;\"></div>\n"
                          "  <a href=\"https://docs.djangoproject.com/en/1.11/topics/testing"
                          "/tools/\"><div class=\"woo-content-wrapper\">\n"
                          "    <div class=\"woo-content \">\n"
                          "      <i class=\"material-icons\">done</i>\n"
                          "      <div>This is woo</div>\n"
                          "    </div>\n"
                          "  </div></a>\n"
                          "</div>")

        self.assertHTMLEqual(output, correct_output)

    def test_custom_gallery_markdown_tags(self):
        test_string = ("Gallery[http://via.placeholder.com/350x150,"
                       "http://via.placeholder.com/350x200, http://via.placeholder.com/350x250,"
                       "http://via.placeholder.com/350x300, http://via.placeholder.com/350x350]")
        output = self.markdown.render(test_string)

        correct_output = ('<p>'
                          '<div class="gallery less">'
                          '  <div class="gallery-content mdl-grid">'
                          '    <div class="gallery-shadow"></div>'
                          '    <div class="mdl-cell mdl-cell--4-col">'
                          '      <img src="http://via.placeholder.com/350x150">'
                          '    </div>'
                          '    <div class="mdl-cell mdl-cell--4-col">'
                          '      <img src="http://via.placeholder.com/350x200">'
                          '    </div>'
                          '    <div class="mdl-cell mdl-cell--4-col">'
                          '      <img src="http://via.placeholder.com/350x250">'
                          '    </div>'
                          '    <div class="mdl-cell mdl-cell--4-col">'
                          '      <img src="http://via.placeholder.com/350x300">'
                          '    </div>'
                          '    <div class="mdl-cell mdl-cell--4-col">'
                          '      <img src="http://via.placeholder.com/350x350">'
                          '    </div>'
                          '  </div>'
                          '  <div class="gallery-more">'
                          '    <button><i class="material-icons">expand_more</i></button>'
                          '  </div>'
                          '  <div class="gallery-less">'
                          '    <button><i class="material-icons">expand_less</i></button>'
                          '  </div>'
                          '</div>'
                          '</p>')

        self.assertHTMLEqual(output, correct_output)
