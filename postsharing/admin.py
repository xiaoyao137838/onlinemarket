from django.contrib import admin
from postsharing.models import Post, Comment, Like, Connection

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Connection)
