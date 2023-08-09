from django.db import models

# Create your models here.

class BaseModel(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Category(BaseModel):
    cat = models.Manager()
    def __str__(self):
        return self.name

class SubCategory(BaseModel):
    
    sub= models.Manager()
    
class Product(BaseModel):
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE,default=None)
    stock = models.PositiveIntegerField(default=0)
    warrenty = models.CharField(max_length=100,blank=True)
    description = models.TextField(max_length=500,blank=True)
    prod = models.Manager()
    
    def __str__(self):
        return self.name