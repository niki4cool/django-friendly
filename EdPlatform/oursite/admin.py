from django.contrib import admin
from .models import Post, Subject, Course, Module, vid
from  embed_video.admin  import  AdminVideoMixin

admin.site.register(Post)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


class vidAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass
admin.site.register(vid, vidAdmin)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
