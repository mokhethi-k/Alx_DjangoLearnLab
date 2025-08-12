from django.contrib import admin
from .models import Post, Comment, Tag
# Register your models here.


#@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'author')
    search_fields = ('title', 'content')
    list_filter = ('published_date', 'tags') 

#@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    #filter_horizontal = ('post',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Tag, TagAdmin)