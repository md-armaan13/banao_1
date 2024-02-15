from django.contrib import admin
from .models import Blog

# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'summary' , 'image' ,'category' , 'drafted' , 'created_at' , 'user' )
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    ordering = ('id',)
