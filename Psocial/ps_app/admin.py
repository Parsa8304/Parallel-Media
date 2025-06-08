from django.contrib import admin
from .models import Persona, Post




@admin.register(Persona)  # Preferred registration method
class PersonaAdmin(admin.ModelAdmin):
    list_display = ['user', 'universe', 'created_at']  # Customize as needed
    search_fields = ['universe', 'tags']
    list_filter = ['created_at']


@admin.register(Post)  # Preferred registration method
class PostAdmin(admin.ModelAdmin):
    list_display = ['persona', 'created_at', 'is_public']
    