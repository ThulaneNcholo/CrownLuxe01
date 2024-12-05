from django.db import models

# Create your models here.
class ProductCatalogModel(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    catalog_image = models.ImageField(
        null=True, blank=True, upload_to='static/images')

    def __str__(self):
        return self.title


class ProductDetailsModel(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class ProductModel(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    available = models.BooleanField(default=True)
    best_sellers = models.BooleanField(default=False)
    product_catalog = models.ForeignKey(ProductCatalogModel, null=True, on_delete=models.CASCADE,
                              blank=True, default=None, related_name='product_catalog')
    product_details = models.ManyToManyField(
        ProductDetailsModel, blank=True, default=None, related_name='product_details')
    cover_image = models.ImageField(
        null=True, blank=True, upload_to='static/images/items')
    image1 = models.ImageField(
        null=True, blank=True, upload_to='static/images/items')
    image2 = models.ImageField(
        null=True, blank=True, upload_to='static/images/items')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name
    

    