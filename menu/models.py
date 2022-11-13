from django.db import models

#MODELS
from accounts.models import (
    User
)
from vendor.models import (
    Vendor
)

# Create your models here.

class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
     
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    # def save(self, *args, **kwargs):
    #     self.category_name = self.category_name.capitalize()
    #     return super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.category_name}"

class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    food_title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='foodImages')
    is_available = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:  
        verbose_name = 'Food Item'
        verbose_name_plural = 'Food Items'
        
    def __str__(self):
        return f"{self.food_title}"
    