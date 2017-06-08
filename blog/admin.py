from django.contrib import admin
from mistune import markdown

# Register your models here.
from .models import Post


class PostAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.compiled_content = markdown(obj.content)
        obj.save()

admin.site.register(Post, PostAdmin)
