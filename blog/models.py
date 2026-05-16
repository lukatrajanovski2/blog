from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    # Старото поле image го оставаме за "главна слика" (thumbnail) на почетната страница, ако сакаш
    image = models.ImageField(upload_to='scammer_pics/', blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

# НОВИОТ МОДЕЛ ШТО ГО ДОДАВАМЕ ПОД КЛАСАТА POST:
class PostImage(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='scammer_pics/')

    def __str__(self):
        return f"Слика за пост: {self.post.title}"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200, default="Анонимен корисник")
    text = models.TextField(verbose_name="Твојот коментар / искуство")
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Коментар од {self.author} на {self.post.title}"