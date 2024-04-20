from django.db import models

# Create your models here.
class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.TextField(null=False, unique=True)
    password = models.TextField(null=False)

    def __str__(self):
        return self.username
    

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField(null=False)
    description = models.TextField(null=False)
    price = models.TextField(null=False)

    def __str__(self):
        return self.title
    

class Image(models.Model):
    id = models.IntegerField(primary_key=True)
    image_uri = models.TextField(null=False)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.image_uri
    

class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(null=False)
    comment = models.TextField(null=False)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.comment
    

class Link(models.Model):
    id = models.IntegerField(primary_key=True)
    no_wa = models.TimeField(null=False)
    web_link = models.TimeField(null=False)
    fb_link = models.TimeField(null=False)
    ig_link = models.TimeField(null=False)
    web_click = models.IntegerField(null=False, default=0)
    fb_click = models.IntegerField(null=False, default=0)
    ig_click = models.IntegerField(null=False, default=0)
    web_checkout = models.IntegerField(null=False, default=0)
    fb_checkout = models.IntegerField(null=False, default=0)
    ig_checkout = models.IntegerField(null=False, default=0)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='links')

    def __str__(self):
        return f"no_wa={self.no_wa}, web_link={self.web_link}, fb_link={self.fb_link}, ig_link={self.ig_link}"


class Date(models.Model):
    id = models.IntegerField(primary_key=True)
    platform = models.TextField(null=False)
    date = models.DateTimeField(null=False)
    id_link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name='dates')

    def __str__(self):
        return str(self.date)