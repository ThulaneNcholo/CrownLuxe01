from django.db import models

# Create your models here.
class ReviewsModel(models.Model):
    FirstName = models.CharField(max_length=200, null=True, blank=True)
    LastName = models.CharField(max_length=200, null=True, blank=True)
    Review = models.TextField(blank=True)
    rating = models.IntegerField(null=True,blank=True) 
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.FirstName