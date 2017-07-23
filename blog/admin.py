from django.contrib import admin
from mistune import Markdown

# Register your models here.
from .models import Post, Page, SocialLink, HeaderImage
from .markdown import PostRenderer, PostInlineLexer

renderer = PostRenderer()
inline = PostInlineLexer(renderer)
inline.enable_woo()
inline.enable_emdash()
inline.enable_figure()

markdown = Markdown(renderer, inline=inline, escape=False)


class PostAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.content = markdown(obj.raw_content)
        obj.save()


admin.site.register(Post, PostAdmin)
admin.site.register(Page)
admin.site.register(SocialLink)
admin.site.register(HeaderImage)
