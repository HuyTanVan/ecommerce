from django.db import models
from django.urls import reverse
from django.conf import settings
import uuid 

# # Create your models here.
# class ProductManager(models.Manager):
#     def get_queryset(self):
#         return super(ProductManager, self).get_queryset().filter(is_active=True)
# class Category(models.Model):
#     name =  models.CharField(max_length=200, db_index=True)
#     slug = models.SlugField(max_length=100, unique=True)
    
#     class Meta:
#         verbose_name_plural = 'categories'
#     def get_absolute_url(self):
#         return reverse('store:category_list', args=[self.slug])
#         # just return a url of a product 
#         # /search/smartphone/
#         # /search/laptop/
#         # /search/smartwatch/ 
#     def __str__(self):
#         return self.name 

# class Product(models.Model):
#     category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_creator')
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(max_length=255)
#     description = models.TextField(blank=False)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     # brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
#     in_stock = models.BooleanField(default=True)
#     stock_quantity = models.IntegerField(default=0)
#     image_url = models.URLField(blank=True)
    
#     is_active = models.BooleanField(default=True) # in case product out of stock, block user to buy
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     objects = models.Manager()
#     products = ProductManager()
#     class Meta:
#         verbose_name_plural = 'products'
#         ordering = ('-created',)
#     def get_absolute_url(self):
#         return reverse('store:product_detail', kwargs={"slug": self.slug})
    
#     def __str__(self):
#         return self.name
# # if __name__=='__main__':
# #     a = Category.objects.create("s", "s")
# #     print(a)
class Category(models.Model):
    name = models.CharField(
            verbose_name=("Category Name"),
            help_text=("Required and unique"),
            max_length=255,
            unique=True,
    )
    slug = models.SlugField(
            
            max_length=255,
            unique=True
    )
    # parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # class MPTTMeta:
    #     order_insertion_by = ['name']

    class Meta:
        verbose_name = ('Category')
        verbose_name_plural = ('Categories')


    def __str__(self):
        return self.name        
    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    slug = models.SlugField()
    is_active = models.BooleanField()

    # Many to Many
    category = models.ManyToManyField(Category)
    
    def __str__(self):
        return f"{self.name} { str(self.category.get())}"
    
    def get_absolute_url(self):
        sku = Inventory.objects.get(product=self.pk)
        sku = sku.sku
        return reverse('store:product_detail', kwargs={"slug": self.slug, "sku": sku})
class Attribute(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    def __str__(self):
        return self.name
class AttributeValue(models.Model):
    value = models.CharField(max_length=50)
    attribute = models.ForeignKey(Attribute, related_name='attribute', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.attribute.name}: {self.value}'
class Inventory(models.Model):
    is_active = models.BooleanField()
    is_default = models.BooleanField()
    product = models.ForeignKey(
        Product, related_name="product", on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    sku_id = str(uuid.uuid4()).split('-')[-1]
    sku = models.CharField(max_length=12, default=sku_id, editable=False)

    
    attribute_values = models.ManyToManyField(AttributeValue)

    class Meta:
        verbose_name_plural = 'Inventory'
    def __str__(self):
        return self.product.name
class StockControl(models.Model):
    last_checked = models.DateTimeField(auto_now_add=True, editable=False)
    units = models.IntegerField(default=0)

    inventory = models.OneToOneField(Inventory, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Stock Control"
class Image(models.Model):
    url = models.ImageField(upload_to=None)
    alternative_text = models.TextField(max_length=50)
    is_feature = models.BooleanField()
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)    
    def __str__(self):
        return self.url
