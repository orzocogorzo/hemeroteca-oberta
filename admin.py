from django.contrib import admin

from .models import (
    Publication,
    Section,
    Signature,
    Article,
    Content,
)

# Register your models here.

admin.site.register(Publication)
admin.site.register(Section)
admin.site.register(Signature)
admin.site.register(Article)
admin.site.register(Content)
