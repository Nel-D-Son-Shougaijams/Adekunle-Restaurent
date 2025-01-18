from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FoodItem(models.Model):
    choices = [
        ("pizza","pizza"),
        ("sushi","sushi"),
        ("salad","salad"),
        ("desert","desert"),
        ("burger","burger"),
        ]
    stat = [
        ("available","available"),
        ("OutOfStock","OutOfStock"),
    ]
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    descriptions = models.TextField()
    category = models.CharField(max_length=200, choices=choices)
    image = models.ImageField()
    img2 = models.ImageField(blank=True,null=True)
    img3 = models.ImageField(blank=True,null=True)
    status = models.CharField(max_length=50, choices=stat,default="available")
    
    def __str__(self):
        return self.name
    
    def description(self):
        return self.descriptions[:40]
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    products = models.JSONField(default=dict)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def merge(self):
        merged_products={}
        for key, product in self.products.items():
            name = product["name"]
            price = product["price"]
            if name in merged_products:
                merged_products[name]["quantity"]+=product["quantity"]
            else:
                merged_products[name] = product
            self.products = merged_products
            self.save()

    def deleteitem(self, product_name):
        for key, product in list(self.products.items()):  # Use list() to avoid runtime errors when modifying the dict
            if product_name == product["name"]:
                product["quantity"] -= 1
                print(self.products[key])
                if product["quantity"] <= 0:
                    del self.products[key]  # Correct way to delete a key from a dictionary
                    print(f"Deleted: {key}")
        self.save()  # Ensure changes are saved

    def total(self):
        """
        Calculate the total price for each item and the total order price.
        Returns a dictionary with detailed pricing information.
        """
        total_order_price = 0
        product_details = {}

        for product_name, details in self.products.items():
            price = float(details["price"])  # Convert price to float
            quantity = int(details["quantity"])  # Convert quantity to integer
            total_price = price * quantity  # Total price for this product
            product_details[product_name] = {
                "name": details["name"],
                "unit_price": price,
                "quantity": quantity,
                "total_price": total_price,
            }
            total_order_price += total_price  # Accumulate total order price

        return total_order_price

class Article(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def sliced(self):
        desc = self.content[:20] + '...'
        return desc
    
class Review(models.Model):
    by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    rating = models.CharField(max_length=50,null=True,blank=True)
    description = models.TextField(max_length=5000)

class Worker(models.Model):
    choices = [
        ("chef","Chef"),
        ("manager","Manager"),
        ("owner","Owner"),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    photo = models.ImageField()
    description = models.TextField()
    staff_level = models.CharField(max_length=50, choices=choices, default="chef")

    def __str__(self):
        return self.user.username
    
    def slcd(self):
        slcd = self.description[:20]
        return slcd
    
class Order(models.Model):
    states = [
        ("notdishpatched","notdishpatched"),
        ("outfordel","outfordel"),
        ("deleivered","deleivered"),
        ("cancelled","cancelled"),
    ]
    product = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True,blank=True)
    current = models.CharField(max_length=50, choices=states, default="notdishpatched")
    details = models.TextField(null=True,blank=True)
    phone_number = models.TextField()
    address = models.TextField()
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    confirm = models.BooleanField(null=True,blank=True)
    items = models.JSONField(null=True,blank=True)


