from django.contrib import admin
from .models import Section, Post, Document, Comment, BlacklistString, Avatar, Cargo, Image

admin.site.register(Section)
admin.site.register(Post)
admin.site.register(Document)
admin.site.register(Comment)
admin.site.register(BlacklistString)
admin.site.register(Avatar)
admin.site.register(Cargo)
admin.site.register(Image)
