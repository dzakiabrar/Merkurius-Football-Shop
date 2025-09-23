import uuid
from django.db import models
# halaman berbeda
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('transfer', 'Transfer'),
        ('update', 'Update'),
        ('exclusive', 'Exclusive'),
        ('match', 'Match'),
        ('rumor', 'Rumor'),
        ('analysis', 'Analysis'),
    ]
    
    # setiap user memiliki halaman yang berbeda
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1) #data lama dikasih user 1
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
    thumbnail = models.URLField(blank=True, null=True)
    news_views = models.PositiveIntegerField(default=0)
    #created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    

    
    def __str__(self):
        return self.title
    
    @property
    def is_news_hot(self):
        return self.news_views > 20
        
    def increment_views(self):
        self.news_views += 1
        self.save()

# class Employe(models.Model):

#     Name = models.CharField(max_length=255)
#     age = models.IntegerField()
#     persona = models.TextField()
