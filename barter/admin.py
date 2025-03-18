from django.contrib import admin
from barter.models import Barter
from django.utils.html import format_html

# Register your models here.


@admin.register(Barter)
class Admin(admin.ModelAdmin):
    search_fields = ["category_name"]

    def _image(self, obj: Barter):
        if obj.barter_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.barter_image.url)
    list_display = ["barter_name", "product", "_image"]
