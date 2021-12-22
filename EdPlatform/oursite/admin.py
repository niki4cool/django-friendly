from django.contrib import admin
from .models import Subject, Course, Module, Video, Post, UrlCheck
from  embed_video.admin  import  AdminVideoMixin

admin.site.register(Post)

admin.site.register(UrlCheck)
class UrlCheckAdmin(admin.ModelAdmin):
    list_display = ['user', 'title']



@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created']
    list_filter = ['created', 'category']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
