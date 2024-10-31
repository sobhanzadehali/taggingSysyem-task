from django.contrib import admin
from .models import Dataset, Tag, Operator, Sentence, HasPermission

# Register your models here.
admin.site.register(Dataset)
admin.site.register(Tag)
admin.site.register(HasPermission)
admin.site.register(Operator)
admin.site.register(Sentence)