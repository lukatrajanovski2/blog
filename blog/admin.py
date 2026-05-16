from django.contrib import admin
from .models import Post, PostImage

# Ова прави полиња за слики едно под друго во истиот екран
class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 3 # Ќе ти даде 3 празни полиња за почеток

# Го регистрираме Post моделот САМО ТУКА
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]