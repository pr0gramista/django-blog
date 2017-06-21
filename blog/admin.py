from django.contrib import admin
from mistune import markdown

# Register your models here.
from .models import Post, Page, SocialLink


class PostAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.content = markdown(obj.raw_content, escape=False)
        obj.save()


admin.site.register(Post, PostAdmin)
admin.site.register(Page)
admin.site.register(SocialLink)
