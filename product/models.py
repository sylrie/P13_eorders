from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    """ Product Category """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ProductTaxe(models.Model):
    """ Product Taxe """
    name = models.CharField(max_length=200)
    value = models.FloatField()

    def __str__(self):
        return str(self.name)+'--'+str(self.value)


class ProductFamily(models.Model):
    """ Product Family """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    """ Product list """

    name = models.CharField(max_length=500, primary_key=True, unique=True)
    img = models.CharField(max_length=300, blank=True)
    details = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    unit_price = models.FloatField(null=False)
    avaiable = models.BooleanField(null=False, default=True)
    #Foreign Key(s)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    family = models.ForeignKey(ProductFamily, blank=True, on_delete=models.CASCADE)
    taxe = models.ForeignKey(ProductTaxe, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)+'--'+str(self.unit_price)+'€ HT'

class ProductManager(models.Model):

    def get_menu(self, family_name=None):
        
        family = []
        category = ProductCategory.objects.all()
        families = (ProductFamily.objects.all())
        for name in families:
            family.append(name)
        items = Product.objects.filter(avaiable=True).order_by('category', 'family', 'unit_price')

        calls = StaffCall.objects.all()
        menu = {
            'category': category,
            'family': family,
            'calls': calls,
            'menu': items
        }

        return menu
    
    def get_product(self, name):
        product = Product.objects.get(name=name)
        return product

class StaffCall(models.Model):
    
    name = models.CharField(max_length=500, primary_key=True, unique=True)
    
    def __str__(self):
        return str(self.name)