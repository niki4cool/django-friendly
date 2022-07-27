from django.contrib import admin
from .models import Subject, Course, Module, Video, Post, UrlCheck, Homework, Constructor, VideoForConstructor, Message, Chat, ImageForUser, Notifications
from  embed_video.admin  import  AdminVideoMixin

admin.site.register(Post)

admin.site.register(Video)

admin.site.register(UrlCheck)

admin.site.register(Message)

admin.site.register(Chat)

admin.site.register(ImageForUser)

admin.site.register(Notifications)

class UrlCheckAdmin(admin.ModelAdmin):
    list_display = ['user', 'title']



@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subj', 'slug']
    prepopulated_fields = {'slug': ('subj',)}




class ModuleInline(admin.StackedInline):
    model = Module
    extra = 0



class HomeworkInLine(admin.StackedInline):
    model = Homework
    extra = 0



class VideoForConstructorAdmin(admin.StackedInline):
    model = VideoForConstructor

@admin.register(Constructor)
class ConstructorAdmin(admin.ModelAdmin):
    list_display = ['owner', 'title', 'description', 'slug']
    inlines = [VideoForConstructorAdmin]

class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created']
    list_filter = ['created', 'category']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline, HomeworkInLine]



admin.site.register(Course, CourseAdmin)
