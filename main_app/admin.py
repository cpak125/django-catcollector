from django.contrib import admin
# import your models here
from .models import Cat, Feeding

# Register your models here.
admin.site.register(Cat)
admin.site.register(Feeding)