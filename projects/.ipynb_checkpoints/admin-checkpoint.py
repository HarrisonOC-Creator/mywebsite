from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Project

admin.site.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "demo_type")
    prepopulated_fields = {"slug": ("title",)}

