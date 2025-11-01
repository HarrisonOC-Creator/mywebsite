# projects/models.py
from django.db import models
from django.utils.text import slugify

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    tech_stack = models.CharField(max_length=300, blank=True, null=True)
    github_link = models.URLField(blank=True)
    demo_type = models.CharField(max_length=50, blank=True, null=True)
    demo_link = models.URLField(blank=True)
    image = models.ImageField(upload_to="projects/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    icon = models.ImageField(upload_to="projects/icons/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title