from django.contrib import admin
from mistune import Markdown

from .models import Post, Page, SocialLink, HeaderImage
from .markdown import PostRenderer, PostInlineLexer

# Add custom markdown renderer
renderer = PostRenderer()
inline = PostInlineLexer(renderer)
inline.enable_woo()
inline.enable_emdash()
inline.enable_figure()

markdown = Markdown(renderer, inline=inline, escape=False)


def publish(modeladmin, request, queryset):
    queryset.update(published=True)
    publish.short_description = "Set to published"


def unpublish(modeladmin, request, queryset):
    queryset.update(published=False)
    unpublish.short_description = "Set to unpublished"


def refresh_markdown(modeladmin, request, queryset):
    refresh_markdown.short_description = "Refresh markdown"

    for q in queryset:
        PostAdmin.save_model(modeladmin, request, q, None, None)


class PostAdmin(admin.ModelAdmin):
    actions = [publish, unpublish, refresh_markdown]

    def save_model(self, request, obj, form, change):
        obj.content = markdown(obj.raw_content)
        obj.save()


admin.site.register(Post, PostAdmin)
admin.site.register(Page)
admin.site.register(SocialLink)
admin.site.register(HeaderImage)
